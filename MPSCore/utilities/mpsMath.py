# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getIntFromString(instr, defaultValue = 0):
	try:
		returnVal = int(instr)
		return returnVal
	except:
		return defaultValue

def getFloatFromString(instr, defaultValue = 0.0):
	try:
		returnVal = float(instr)
		return returnVal
	except:
		return defaultValue
