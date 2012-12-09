# -*- coding:utf-8 -*-
import sys
import sublime, sublime_plugin
import thread
import json
import urllib
import urllib2

import xml.dom.minidom        

reload(sys)

sys.setdefaultencoding("utf-8")

#Bing translator
class BingTranslatorSettings:
	view_id = None
	
	oauth_end_point="https://datamarket.accesscontrol.windows.net/v2/OAuth2-13";
	translate_end_point = "http://api.microsofttranslator.com/v2/Http.svc/Translate"
       
	client_id = "SublimeBingTranslator"
	client_secret = "0fjvxMgcSZreEk9xPN8Vse+KDz3XlI+W11XJxC8peEA="
	scope = "http://api.microsofttranslator.com"
	grant_type = "client_credentials"

	#Translator Language Codes
	#http://msdn.microsoft.com/en-us/library/hh456380.aspx
	_from = "en"
	to = "ja"

#global settings
settings = BingTranslatorSettings()

class BingTranslator:
	def translate(self, command, edit, _from, to):
		sublime.status_message("start translate...")
		#todo create thread
		sels = command.view.sel()
		source_text = ""
		last_sel = None
		for sel in sels:
			source_text += command.view.substr(sel)+" "
			last_sel = sel
		if len(source_text) == 1:
			sublime.status_message("not selected. do not translate")
			return
		sublime.status_message("get token...")
		token = self.getOAuthToken()
		sublime.status_message("translate...")
		translated = self.doTranslate(source_text, _from, to, token)

		self.showResult(edit, source_text, translated)
		sublime.status_message("translate end...")
	def getResultView(self):
		global settings
		active_window = sublime.active_window()
		for view in active_window.views():
			if view.id() == settings.view_id:
				return view
		new_view = active_window.new_file()
		settings.view_id = new_view.id()
		new_view.set_name("Bing Transrator Results.")
		return new_view

	def showResult(self, edit, source_text, translated):
		view = self.getResultView()
		result = "*translate*\n"
		result += "------------------------\n"
		result += source_text + "\n"
		result += "- - - - - - - - - - - - \n"
		result += translated + "\n"
		result += "------------------------\n"
		result += "\n"
		view.insert(edit, 0, result)

		sublime.active_window().focus_view(view)
	def getOAuthToken(self):
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
	def run(self, edit):
		global settings
		BingTranslator().translate(self, edit, settings.to, settings._from)
	def description(self, args):
		return "bing translator plugin reverse"

class SelectTranslateCommand(sublime_plugin.TextCommand):
	translator = BingTranslator()
	def run(self, edit):
		global settings
		self.translator.translate(self, edit, settings._from, settings.to)
	def description(self, args):
		return "bing translator plugin"

