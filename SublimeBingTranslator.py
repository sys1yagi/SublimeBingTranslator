import sublime, sublime_plugin
import thread
import json
#MStranslate

class SelectTranslateCommand(sublime_plugin.WindowCommand):
	def run(self):
		#self.view.insert(edit, 0, u"Hello, World")
		#sels = self.view.sel()
		sublime.status_message('morusuaaaa...')
		#for sel in sels:
		#	self.view.insert(edit, 0, self.view.substr(sel))

	def description(self, args):
		return "ms translate"


