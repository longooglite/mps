# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

class ConfigUtilities():

	#	Configuration Utility class.

	def loadConfig(self, _configFilePath, _seedConfig):
		with open(_configFilePath, 'r') as configFile:
			specifiedJsonData = configFile.read()
		specifiedDict = json.loads(specifiedJsonData)
		for key in specifiedDict.keys():
			_seedConfig[str(key).strip().lower()] = specifiedDict[key]
		return _seedConfig

	def addURLMappingsFromModule(self, _module, _urlMappingsList):
		for each in _module.urlMappings:
			_urlMappingsList.append(each)
