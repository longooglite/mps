# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import codecs
srcFile = codecs.open('/Users/erpaul/Desktop/eastywesty40000dolluhplease.txt', 'r', 'utf-8', errors='ignore')

for line in srcFile:
	splits = line.split(',')
	pcn = splits[0].strip()
	ew = splits[1].strip()[0].upper()
	newPcn = '''%s%s%s''' % (pcn[0:2],ew,pcn[2:])
	print "UPDATE roster_item SET pcn = '%s' WHERE pcn = '%s';" % (newPcn,pcn)
	print "UPDATE position SET pcn = '%s' WHERE pcn = '%s';" % (newPcn,pcn)
	print "UPDATE position_list_item SET pcn = '%s' WHERE pcn = '%s';" % (newPcn,pcn)
