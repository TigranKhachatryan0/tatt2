#!/usr/bin/env python3

from PluginCommon import PluginInfo, CliHandler
import base64

class Info(PluginInfo):
	def __init__(self):
		self.name = "Base32"
		self.description = "Binary-to-text data encoding mechanism, known for case insensivity"

def encode(**kwargs):
	text = kwargs["data"].encode()
	ret = base64.b32encode(text).decode("utf-8")
	return ret

def decode(**kwargs):
	text = kwargs["data"]
	ret = base64.b32decode(text).decode("utf-8")
	return ret

if __name__ == '__main__':
	plugin_info=Info()
	CliHandler(plugin_info, encode, decode)
