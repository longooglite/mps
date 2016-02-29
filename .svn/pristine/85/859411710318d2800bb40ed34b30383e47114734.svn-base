# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from Crypto.Cipher import AES
import base64

kIv456 = "&^yhVcDW2#12-+]["
kKey = "&yjs#Rbv(*7^&%RFD@!Qascvm.P:LKIU"

def encrypt(plain_text):
	if plain_text:
		justificationLen = 16
		while justificationLen < len(plain_text):
			justificationLen += 16
		paddedText = plain_text.rjust(justificationLen)
		encryption_suite = AES.new(kKey, AES.MODE_CBC, kIv456)
		return base64.b64encode(encryption_suite.encrypt(paddedText))
	return ''

def decrypt(cipher_text):
	if cipher_text:
		decryption_suite = AES.new(kKey, AES.MODE_CBC, kIv456)
		return decryption_suite.decrypt(base64.b64decode(cipher_text)).strip()
	return ''
