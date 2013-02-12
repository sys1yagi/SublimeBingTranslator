# -*- coding:utf-8 -*-
import sublime, sublime_plugin
import sys
import threading
import json
import urllib
import urllib2
import xml.dom.minidom        

reload(sys)

sys.setdefaultencoding("utf-8")

#Bing translator
class BingTranslatorSettings:
	view_id = None
	thread = None
	oauth_end_point="https://datamarket.accesscontrol.windows.net/v2/OAuth2-13";
	translate_end_point = "http://api.microsofttranslator.com/v2/Http.svc/Translate"
	client_id = "SublimeBingTranslator"
	client_secret = "0fjvxMgcSZreEk9xPN8Vse+KDz3XlI+W11XJxC8peEA="
	scope = "http://api.microsofttranslator.com"
	grant_type = "client_credentials"


#global settings
settings = BingTranslatorSettings()
translate_settings = sublime.load_settings("Bing Translator.sublime-settings");	

class BingTranslator:
	def __call__(self, command, edit, source_text, _from, to):
		"""
		Translating text typed language.

		Args:
        	command: sublime text command object.
        	edit: sublime text edit object.
        	source_text: String to be translated.
        	_from: Language of the string to translate.
        	to: to Language.
    		Returns: None.
		"""
		sublime.set_timeout(lambda: sublime.status_message("translate...."), 100)
		token = self.get_oauth_token()
		translated = self.doTranslate(source_text, _from, to, token)
		sublime.set_timeout(lambda:self.show_result(edit, source_text, translated), 100)
	def translate(self, command, edit, _from, to):
		"""
		TODO
		Args:
			command:
			edit:
			_from:
			to:

		"""
		global settings
		sublime.status_message("start translate...")
		sels = command.view.sel()
		source_text = ""
		last_sel = None
		for sel in sels:
			source_text += command.view.substr(sel)+" "
			last_sel = sel
		if len(source_text) == 1:
			sublime.status_message("not selected. can't translate.")
			return
		if settings.thread != None and settings.thread.isAlive() == True:
			sublime.status_message("already translate now. wait please.")
			return
		settings.thread = threading.Thread(target=self, args=(command, edit, source_text, _from, to,))
		settings.thread.setDaemon(True)
		settings.thread.start()

	def get_result_view(self):
		"""
			To get the file to display the translation results.
			start a thread and translate.
		"""
		global settings
		active_window = sublime.active_window()
		for view in active_window.views():
			if view.id() == settings.view_id:
				return view
		new_view = active_window.new_file()
		settings.view_id = new_view.id()
		new_view.set_name("Bing Transrator Results.")
		new_view.set_scratch(translate_settings.get("scratch"))
		return new_view

	def show_result(self, edit, source_text, translated):
		view = self.get_result_view()
		result = "*translate*\n"
		result += "------------------------\n"
		result += source_text + "\n"
		result += "- - - - - - - - - - - - \n"
		result += translated + "\n"
		result += "------------------------\n"
		result += "\n"
		view.insert(edit, 0, result)

		sublime.active_window().focus_view(view)
	def get_oauth_token(self):
		global settings
		request_data = {}
		request_data["client_id"] = settings.client_id
		request_data["client_secret"] = settings.client_secret
		request_data["scope"] = settings.scope
		request_data["grant_type"] = settings.grant_type

		params = urllib.urlencode(request_data)
		handle = urllib.urlopen(settings.oauth_end_point, params)
		json_data = handle.read()
		handle.close()
		json_obj = json.loads(json_data)

		return json_obj["access_token"]

	def doTranslate(self, text, _from, to, token):
		global settings
		request_data = {}
		request_data["Text"] = text
		request_data["To"] = to
		request_data["From"] = _from
		params = urllib.urlencode(request_data)

		request = urllib2.Request(settings.translate_end_point+"?"+params)
		request.add_header('Authorization', 'Bearer '+ token)

		response = urllib2.urlopen(request)
		content = response.read()
		dom = xml.dom.minidom.parseString(content)
		translated = ""
		for elem in dom.getElementsByTagName("string"):
			if elem.firstChild != None:
				translated = elem.firstChild.nodeValue
		return translated.encode("utf-8")

class SelectTranslateReverseCommand(sublime_plugin.TextCommand):
	translator = BingTranslator()
	def __init__(self, *args, **kwargs):
		sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
	def run(self, edit):
		global settings
		global translate_settings
		self.translator.translate(self, edit, translate_settings.get("to"), translate_settings.get("from"))
	def description(self, args):
		return "bing translator plugin reverse"

class SelectTranslateCommand(sublime_plugin.TextCommand):
	translator = BingTranslator()
	def __init__(self, *args, **kwargs):
		sublime_plugin.TextCommand.__init__(self, *args, **kwargs)
		self.setting = sublime.load_settings("SublimeBingTranslator.sublime-settings");
	def run(self, edit):
		global settings
		global translate_settings
		self.translator.translate(self, edit, translate_settings.get("from"), translate_settings.get("to"))
	def description(self, args):
		return "bing translator plugin"

