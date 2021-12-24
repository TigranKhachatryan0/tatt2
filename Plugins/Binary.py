#!/usr/bin/env python3

from PluginCommon import PluginInfo, CliHandler
import base64

class Info(PluginInfo):
	def __init__(self):
		self.name = "Binary"
		self.description = "Creates binary represantations of each character, separated by space"

def encode(**kwargs):
	text = kwargs["data"]
	ret = str()
	for character in text:
		binary = str(bin(ord(character)))[2:]
		ret += binary + " "
	return ret[:-1]

def decode(**kwargs):
	text = kwargs["data"]
	if text == "":
		return ""
	ret = str()
	for c,binary_str in enumerate(text.split(" ")):
		try:
			binary = int(f"0b{binary_str}", 2)
		except:
			raise ValueError(f"Invalid binary character at word {c+1}.")
		ret += chr(binary)
	return ret

if __name__ == '__main__':
	plugin_info=Info()
	CliHandler(plugin_info, encode, decode)
