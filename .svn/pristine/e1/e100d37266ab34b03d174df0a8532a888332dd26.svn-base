# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#   Various dictionary-related utilities.

def copyKeysWithPrefix(_fromDict, _toDict, _prefix):
	if not _fromDict: return
	if not _prefix: return
	if _toDict is None: return

	for key in _fromDict.keys():
		if key.startswith(_prefix):
			_toDict[key] = _fromDict[key]

