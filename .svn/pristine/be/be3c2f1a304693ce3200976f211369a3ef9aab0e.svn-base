# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSAppt.core.sql.packetSQL as pSQL

def getPacketMeta(_dbConnection, _packetCode):
	packetMetaDict = {}
	rawMeta = pSQL.getPacketMeta(_dbConnection,_packetCode)
	if rawMeta:
		packetMetaDict['packet_title'] = rawMeta[0].get('packet_descr')
		packetMetaDict['groups'] = []
		currentGroup = {"code":None}
		for group in rawMeta:
			if currentGroup.get('code',None) <> group.get('group_code',''):
				currentGroup = {}
				currentGroup['code'] = group.get('group_code','')
				currentGroup['descr'] = group.get('group_descr','')
				currentGroup['items'] = []
				packetMetaDict['groups'].append(currentGroup)
			item = {}
			item['item_code'] = group.get('item_code','')
			item['seq'] = 1
			item['is_artifact'] = group.get('is_artifact','')
			item['artifact_config_dict'] = group.get('artifact_config_dict','')
			currentGroup['items'].append(item)
	return packetMetaDict