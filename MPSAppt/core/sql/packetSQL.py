# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getPacketMeta(_dbConnection,_packetCode):
	sql = '''SELECT p.code AS packet_code, p.descr AS packet_descr,
			g.code AS group_code, g.descr AS group_descr,g.seq AS group_seq,
			i.item_code AS item_code, i.seq AS item_seq, i.is_artifact as is_artifact,
			i.artifact_config_dict as artifact_config_dict
			FROM wf_packet p,wf_packet_group g,wf_packet_item i
			WHERE g.packet_id = p.id AND i.packet_group_id = g.id and p.code = %s
			ORDER BY group_seq,item_seq ASC;'''
	return _dbConnection.executeSQLQuery(sql, (_packetCode,))
