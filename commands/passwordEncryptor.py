# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import sys
import hashlib

def encryptValue(_value):
	valu = hashlib.sha256()
	valu.update(_value)
	return valu.hexdigest()

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: python passwordEncryptor <valueToEncrypt>"
		exit()
	value = sys.argv[1]
	print "%s = %s" % (value, encryptValue(value))
