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
	oauth_end_point="https://datamarket.accesscontrol.windows.net/v2/OAuth2-13";
	translate_end_point = "http://api.microsofttranslator.com/v2/Http.svc/Translate"
       
	client_id = "SublimeBingTranslator"
	client_secret = "0fjvxMgcSZreEk9xPN8Vse+KDz3XlI+W11XJxC8peEA="
	scope = "http://api.microsofttranslator.com"
	grant_type = "client_credentials"

	_from = "en"
	to = "ja"


class SelectTranslateCommand(sublime_plugin.TextCommand):
	
	settings = BingTranslatorSettings()
	#work_thread = thread()

	def run(self, edit):
		sublime.status_message("start translate...")
		#todo create thread
		#self.active_window().show_quick_panel([["moge"], ["hugs"], self.on_done)

		sels = self.view.sel()
		text = ""
		last_sel = None
		for sel in sels:
			text += self.view.substr(sel)+" "
			last_sel = sel
		if len(text) == 1:
			sublime.status_message("not selected. do not translate")
			return
		sublime.status_message("get token...")
		token = self.getOAuthToken()
		sublime.status_message("translate...")
		translated = self.translate(text, self.settings._from, self.settings.to, token)
		
		#self.view.insert(edit, last_sel.a if last_sel.b < last_sel.a else last_sel.b , "\n"+translated)
		#self.window.show_quick_panel([["moge"], ["hugs"]], self.on_done)
 		
 		#self.view.window().show_quick_panel([translated], None, sublime.MONOSPACE_FONT)
		
		sublime.status_message("translate end...")
		
#	def on_done(self, picked):
#		pass

	def description(self, args):
		return "bing translate"

	def getOAuthToken(self):
		request_data = {}
		request_data["client_id"] = self.settings.client_id
		request_data["client_secret"] = self.settings.client_secret
		request_data["scope"] = self.settings.scope
		request_data["grant_type"] = self.settings.grant_type

		params = urllib.urlencode(request_data)
		handle = urllib.urlopen(self.settings.oauth_end_point, params)
		json_data = handle.read()
		handle.close()
		json_obj = json.loads(json_data)

		return json_obj["access_token"]

	def translate(self, text, _from, to, token):
		request_data = {}
		request_data["Text"] = text
		request_data["To"] = to
		request_data["From"] = _from
		params = urllib.urlencode(request_data)

		request = urllib2.Request(self.settings.translate_end_point+"?"+params)
		request.add_header('Authorization', 'Bearer '+ token)

		response = urllib2.urlopen(request)
		content = response.read()
		dom = xml.dom.minidom.parseString(content)
		translated = ""
		for elem in dom.getElementsByTagName("string"):
			if elem.firstChild != None:
				translated = elem.firstChild.nodeValue
		return translated.encode("utf-8")

