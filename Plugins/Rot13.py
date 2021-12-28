#!/usr/bin/env python3

from PluginCommon import PluginInfo, CliHandler

class Info(PluginInfo):
	def __init__(self):
		self.name = "ROT-13"
		self.description = "Rotates each letter 13 times"

alphabet_upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_lower=alphabet_upper.lower()

def encode(**kwargs):
	text = kwargs["data"]
	ret = ""
	for letter in text:
		if letter.upper() in alphabet_upper:
			letter_index = alphabet_upper.index(letter.upper())
			letter_index += 13
			if letter_index>=26:
				letter_index -= 26
			if letter.upper() == letter:
				ret += alphabet_upper[letter_index]
			else:
				ret += alphabet_lower[letter_index]
		else:
			ret += letter
	return ret

def decode(**kwargs):
	text = kwargs["data"]
	ret = encode(data=text)
	return ret

if __name__ == '__main__':
	plugin_info=Info()
	CliHandler(plugin_info, encode, decode)
