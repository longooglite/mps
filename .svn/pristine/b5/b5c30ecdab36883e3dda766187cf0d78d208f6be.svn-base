# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
atramLoad.py
'''

import sys
import os
import os.path
import csv
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import string
import logging
import logging.config
import optparse
import json
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.stringUtilities as stringUtils
import MPSCore.utilities.mpsMath as mpsMath
import MPSCore.core.constants

import cStringIO

kDelimiter = "|"

#inserts
kMetaTrackInsertSQL = "INSERT INTO wf_metatrack (code,descr,supplemental,active,tags) VALUES (%s,%s,%s,%s,%s)"
kTrackInsertSQL = "INSERT INTO wf_track (code,descr,active,metatrack_id,tags) VALUES (%s,%s,%s,%s,%s)"
kTitleInsertSQL = "INSERT INTO wf_title (code,descr,active,job_code,track_id,position_criteria,rank_order,isactionable,tags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
kDepartmentInsertSQL = '''INSERT INTO wf_department (code,descr,active,parent_id,pcn_id,cc_acct_cd,header_image,email_address,address_lines,address_suffix,city,state,postal) VALUES (%s,%s,'t',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
kDepartmentChairInsertSQL = '''INSERT INTO wf_department_chair (department_id,chair_with_degree,chair_signature,chair_titles,seq) VALUES (%s,%s,%s,%s,%s)'''
kAppointmentStatusInsertSQL = '''INSERT INTO wf_appointment_status (code,descr) VALUES (%s,%s)'''
kComponentTypeInsertSQL = '''INSERT INTO wf_component_type (code,descr) VALUES (%s,%s)'''
kJobActionTypeInsertSQL = '''INSERT INTO wf_job_action_type (code,descr,active) VALUES (%s,%s,%s)'''
kPacketInsertSQL = '''INSERT INTO wf_packet (code,descr) VALUES (%s,%s)'''
kPacketGroupInsertSQL = '''INSERT INTO wf_packet_group (code,descr,seq,packet_id) VALUES (%s,%s,%s,%s)'''
kPacketItemInsertSQL = '''INSERT INTO wf_packet_item (item_code,seq,packet_group_id,is_artifact,artifact_config_dict) VALUES (%s,%s,%s,%s,%s)'''
kQuestionInsertSQL = 'INSERT INTO wf_question (task_code,code,prompt,required,seq,active,identifier_code,nbr_rows) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
kQuestionOptionInsertSQL = 'INSERT INTO wf_question_option (question_id,code,option_text,has_text,text_title,text_required,seq,active,nbr_rows) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
kEvaluatorTypeInsertSQL = 'INSERT INTO wf_evaluator_type (code,descr,is_external,is_arms_length,requires_approval) VALUES (%s,%s,%s,%s,%s)'
kEvaluatorSourceInsertSQL = 'INSERT INTO wf_evaluator_source (code,descr) VALUES (%s,%s)'
kTerminationTypeInsertSQL = 'INSERT INTO wf_termination_type (code,descr) VALUES (%s,%s)'
kUberQuestionInsertSQL = 'INSERT INTO wf_uber_question (code,descr,display_text,header_text,cols_offset,cols_label,cols_prompt,required,wrap,encrypt,data_type,data_type_attributes,job_action_types,identifier_code,show_codes,hide_codes) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
kUberOptionInsertSQL = 'INSERT INTO wf_uber_option (uber_question_id,code,descr,display_text,seq,show_codes,hide_codes) VALUES (%s,%s,%s,%s,%s,%s,%s)'
kUberGroupInsertSQL = 'INSERT INTO wf_uber_group (code,descr,display_text,cols_offset,cols_label,repeating,repeating_table,required,wrap,filler,children) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
kTrackChangeInsertSQL = 'INSERT INTO wf_track_change (workflow_code,code,descr) VALUES (%s,%s,%s) RETURNING id'
kTrackChangeMapInsertSQL = "INSERT INTO wf_track_change_map (track_change_id,from_track_id,to_track_id,from_title_id,to_title_id) VALUES (%s,%s,%s,%s,%s)"
kBuildingInsertSQL = '''INSERT INTO wf_building (code,descr,address_lines,city,state,country,postal,active) values (%s,%s,%s,%s,%s,%s,%s,'t');'''
kStaticLookupInsertSQL = '''INSERT INTO cv_static_lookup (lookup_key,code,descr,alt_descr,seq) VALUES (%s, %s, %s, %s, %s);'''

#updates
kMetaTrackUpdateSQL = "UPDATE wf_metatrack SET descr = %s,supplemental = %s,active = %s, tags = %s WHERE code = %s"
kTrackUpdateSQL = "UPDATE wf_track SET descr = %s,active = %s,metatrack_id = %s,tags = %s WHERE code = %s"
kTitleUpdateSQL = "UPDATE wf_title SET descr = %s,active = %s,job_code = %s,track_id = %s,position_criteria = %s,rank_order = %s, isactionable = %s, tags = %s WHERE code = %s"
kDepartmentUpdateSQL = '''UPDATE wf_department SET descr = %s,parent_id = %s,pcn_id = %s,cc_acct_cd = %s,header_image = %s,email_address = %s,address_lines = %s,address_suffix = %s,city = %s,state = %s,postal = %s WHERE code = %s'''
kDepartmentChairUpdateSQL = '''UPDATE wf_department_chair SET chair_with_degree = %s,chair_signature = %s,chair_titles = %s WHERE department_id = %s AND seq = %s'''
kAppointmentStatusUpdateSQL = '''UPDATE wf_appointment_status SET descr = %s WHERE code = %s'''
kComponentTypeUpdateSQL = '''UPDATE wf_component_type SET descr = %s WHERE code = %s'''
kJobActionTypeUpdateSQL = '''UPDATE wf_job_action_type SET descr = %s,active = %s WHERE code = %s'''
kPacketUpdateSQL = '''UPDATE wf_packet set descr = %s WHERE code = %s'''
kPacketGroupUpdateSQL = '''UPDATE wf_packet_group SET descr = %s, seq = %s WHERE code = %s AND packet_id = %s'''
kPacketItemUpdateSQL = '''UPDATE wf_packet_item SET seq = %s, is_artifact = %s, artifact_config_dict = %s WHERE item_code = %s AND packet_group_id = %s'''
kQuestionUpdateSQL = 'UPDATE wf_question SET task_code = %s,prompt = %s,required = %s,seq = %s,active = %s,identifier_code = %s,nbr_rows = %s WHERE code = %s'
kQuestionOptionUpdateSQL = 'UPDATE wf_question_option SET question_id = %s,option_text = %s,has_text = %s, text_title = %s, text_required = %s,seq = %s,active = %s,nbr_rows = %s WHERE code = %s'
kEvaluatorTypeUpdateSQL = 'UPDATE wf_evaluator_type SET descr=%s, is_external=%s, is_arms_length=%s, requires_approval=%s WHERE code = %s'
kEvaluatorSourceUpdateSQL = 'UPDATE wf_evaluator_source SET descr=%s WHERE code = %s'
kTerminationTypeUpdateSQL = 'UPDATE wf_termination_type SET descr=%s WHERE code = %s'
kUberQuestionUpdateSQL = 'UPDATE wf_uber_question SET descr=%s,display_text=%s,header_text=%s,cols_offset=%s,cols_label=%s,cols_prompt=%s,required=%s,wrap=%s,encrypt=%s,data_type=%s,data_type_attributes=%s,job_action_types=%s,identifier_code=%s,show_codes=%s,hide_codes=%s WHERE code=%s'
kUberOptionUpdateSQL = 'UPDATE wf_uber_option SET uber_question_id=%s,descr=%s,display_text=%s,seq=%s,show_codes=%s,hide_codes=%s WHERE code=%s'
kUberGroupUpdateSQL = 'UPDATE wf_uber_group SET descr=%s,display_text=%s,cols_offset=%s,cols_label=%s,repeating=%s,repeating_table=%s,required=%s,wrap=%s,filler=%s,children=%s WHERE code=%s'
kBuildingUpdateSQL = '''UPDATE wf_building SET descr = %s,address_lines = %s,city = %s,state = %s,country = %s,postal = %s,active = 't' WHERE code = %s;'''
kStaticLookupUpdateSQL = '''UPDATE cv_static_lookup SET descr = %s,alt_descr = %s,seq = %s WHERE lookup_key = %s AND code = %s;'''

class AtramLoad(object):
	logger = logging.getLogger(__name__)

	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'dev'
		self.user = 'mps'
		self.password = 'mps'
		self.db = None
		self.messageList = []
		self.site = 'dev'
		self.destroy = '0'
		self.optiononly = ''

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.site: self.site = options.site
			if options.destroy: self.destroy = options.destroy
			if options.optiononly: self.optiononly = options.optiononly


	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		try:
			self.connectToDatabase()
			if not self.optiononly:
				self.destroyData()
				self.importMetaTracks()
				self.importTracks()
				self.importTitles()
				self.importTitles2()
				self.importDepartments()
				self.importDepartments2()
				self.importDepartmentChairs()
				self.importDepartmentChairs2()

				self.importAppointmentStatuses()
				self.importComponentTypes()
				self.importJobActionTypes()
				self.importEvaluatorTypes()
				self.importEvaluatorSources()
				self.importOracleTable()
				self.importTerminationType()
				self.importTrackChangeMap()
				self.importBuildings()
				self.updateGenericStaticLookup('FPSC','fpsc.txt')
				self.updateGenericStaticLookup('CRED_DEPTS','cred_depts.txt')
				self.updateGenericStaticLookup('CRED_PROGRAMS','cred_programs.txt')
			if not self.optiononly or self.optiononly == 'packet':
				self.importPackets()
			if not self.optiononly or self.optiononly == 'rfp':
				self.importRFP()
			if not self.optiononly or self.optiononly == 'uber':
				self.importUber()
		except Exception, e:
			print e.message
			logger = logging.getLogger(__name__)
			logger.exception(e.message)
			sys.exit(999)

	def destroyData(self):
		if self.destroy == "1":
			self.db.executeSQLCommand("delete from wf_job_action;")
			self.db.executeSQLCommand("delete from wf_appointment;")
			self.db.executeSQLCommand("delete from wf_position;")
			self.db.executeSQLCommand("delete from wf_workflow_metatrack;")
			self.db.executeSQLCommand("delete from wf_workflow;")
			self.db.executeSQLCommand("delete from wf_title;")
			self.db.executeSQLCommand("delete from wf_track;")
			self.db.executeSQLCommand("delete from wf_metatrack;")
			self.db.executeSQLCommand("delete from wf_username_department;")
			self.db.executeSQLCommand("delete from wf_department_chair;")
			self.db.executeSQLCommand("delete from wf_department;")
			self.db.executeSQLCommand("delete from wf_pcn;")
			self.db.executeSQLCommand("delete from wf_appointment_status;")
			self.db.executeSQLCommand("delete from wf_packet_item;")
			self.db.executeSQLCommand("delete from wf_packet_group;")
			self.db.executeSQLCommand("delete from wf_packet;")
			self.db.executeSQLCommand("delete from wf_question_response;")
			self.db.executeSQLCommand("delete from wf_question_option;")
			self.db.executeSQLCommand("delete from wf_question;")
			self.db.executeSQLCommand("delete from wf_evaluator_type;")
			self.db.executeSQLCommand("delete from wf_uber_option;")
			self.db.executeSQLCommand("delete from wf_uber_question;")
			self.db.executeSQLCommand("delete from wf_uber_group;")

	#static lookup data

	def getCode(self,instr):
		allowed = string.letters + string.digits
		returnVal = ""
		for each in instr:
			if allowed.find(each) > -1:
				returnVal += each
		return returnVal

	def updateGenericStaticLookup(self,lookupKey,fileName):
		rawData = self.getImportFileBySite(fileName, delimit='|')
		i = 0
		for rawRow in rawData:
			if self.rowValid(rawRow):
				i += 1
				items = rawRow
				code = self.getCode(items[0])
				self.upsertStaticLookup(lookupKey,code,items[1].strip(),'',i)

	def upsertStaticLookup(self,lookupKey,code,descr,alt_descr,seq):
		whereClause = "lookup_key = '%s' AND code = '%s'" % (lookupKey,code)
		if self.db.getRowCount('cv_static_lookup', whereClause):
			self.db.executeSQLCommand(kStaticLookupUpdateSQL,(descr,
															alt_descr,
															seq,
															lookupKey,
															code))
		else:
			self.db.executeSQLCommand(kStaticLookupInsertSQL,(lookupKey,
														   code,
															descr,
															alt_descr,
															seq))

	def importBuildings(self):
		#code,descr,address_lines,city,state,country,postal,phone,fax,email
		fileData = [['A','Building A','["Address A 1", "Address A 2"]','Ann Arbor','MI','UnitedStatesofAmerica','48103'],
					['B','Building B','["Address B 1", "Address B 2", "Address B-3"]','Chelsea','MI','UnitedStatesofAmerica','48117']]

		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				address_lines = row[2]
				city = row[3]
				state = row[4]
				country = row[5]
				postal = row[6]
				tableKey = self.getTableKey("wf_building", code)
				if tableKey is not None:
					args = (descr,address_lines,city,state,country,postal,code,)
					self.db.executeSQLCommand(kBuildingUpdateSQL, args)
				else:
					args = (code,descr,address_lines,city,state,country,postal,)
					self.db.executeSQLCommand(kBuildingInsertSQL, args)


	def importTrackChangeMap(self):
		fileData = self.getImportFileBySite("track_change_map.txt", delimit='|')
		if fileData:
			self.db.executeSQLCommand("DELETE FROM wf_track_change_map")
			self.db.executeSQLCommand("DELETE FROM wf_track_change")
		rowNbr = 0
		for row in fileData:
			if self.rowValid(row):
				rowNbr += 1
				workflow_code = row[0]
				code = row[1]
				descr = row[2]
				fromTrackCode = row[3]
				toTrackCode = row[4]
				fromTitleCode = self.manufactureCode([fromTrackCode,row[5],])
				toTitleCode = self.manufactureCode([toTrackCode,row[6],])
				trackChangeId = self.getTableKey('wf_track_change',code)
				if not trackChangeId:
					trackChangeId = self.db.executeSQLQuery(kTrackChangeInsertSQL,(workflow_code,code,descr,))[0]['id']
					self.db.executeSQLCommand('commit')
				fromTrackCodeId = self.getTableKey('wf_track',fromTrackCode)
				toTrackCodeId = self.getTableKey('wf_track',toTrackCode)
				fromTitleId = self.getTableKey('wf_title',fromTitleCode)
				toTitleId = self.getTableKey('wf_title',toTitleCode)
				if (fromTrackCodeId and toTrackCodeId and fromTitleId and toTitleId):
					pass
				else:
					print "unable to create track change map for %s %s->%s" % (code,fromTrackCode,toTrackCode)
				self.createTrackChangeMap(trackChangeId,fromTrackCodeId,toTrackCodeId,fromTitleId,toTitleId)


	def createTrackChangeMap(self,trackChangeId,fromTrackCodeId,toTrackCodeId,fromTitleId,toTitleId):
		args = (trackChangeId,fromTrackCodeId,toTrackCodeId,fromTitleId,toTitleId,)
		self.db.executeSQLCommand(kTrackChangeMapInsertSQL,args)

	def importUber(self):
		self.importUberQuestions()
		self.importUberOptions()
		self.importUberGroups()

	def importUberQuestions(self):
		fileData = self.getImportFileBySite("uberQuestions.txt", delimit='\t')
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				display_text = row[2]
				header_text = row[3]
				cols_offset = row[4]
				cols_label = row[5]
				cols_prompt = row[6]
				required = row[7]
				wrap = row[8]
				encrypt = row[9]
				data_type = row[10]
				data_type_attributes = row[11]
				job_action_types = row[12]
				identifier_code = row[13]
				show_codes = row[14]
				hide_codes = row[15]

				tableKey = self.getTableKey("wf_uber_question", code)
				if tableKey is not None:
					args = (descr,display_text,header_text,cols_offset,cols_label,cols_prompt,required,wrap,encrypt,data_type,data_type_attributes,job_action_types,identifier_code,show_codes,hide_codes,code,)
					self.db.executeSQLCommand(kUberQuestionUpdateSQL, args)
				else:
					args = (code,descr,display_text,header_text,cols_offset,cols_label,cols_prompt,required,wrap,encrypt,data_type,data_type_attributes,job_action_types,identifier_code,show_codes,hide_codes,)
					self.db.executeSQLCommand(kUberQuestionInsertSQL, args)

	def importUberOptions(self):
		fileData = self.getImportFileBySite("uberOptions.txt", delimit='\t')
		for row in fileData:
			if self.rowValid(row):
				question_code = row[0]
				code = row[1]
				descr = row[2]
				display_text = row[3]
				seq = row[4]
				show_codes = row[5]
				hide_codes = row[6]

				question_id = self.getTableKey("wf_uber_question", question_code)
				tableKey = self.getTableKey("wf_uber_option", code)
				if tableKey is not None:
					args = (question_id,descr,display_text,seq,show_codes,hide_codes,code,)
					self.db.executeSQLCommand(kUberOptionUpdateSQL, args)
				else:
					args = (question_id,code,descr,display_text,seq,show_codes,hide_codes,)
					self.db.executeSQLCommand(kUberOptionInsertSQL, args)

	def importUberGroups(self):
		fileData = self.getImportFileBySite("uberGroups.txt", delimit='\t')
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				display_text = row[2]
				cols_offset = row[3]
				cols_label = row[4]
				repeating = row[5]
				repeating_table = row[6]
				required = row[7]
				wrap = row[8]
				filler = row[9]
				children = row[10]

				tableKey = self.getTableKey("wf_uber_group", code)
				if tableKey is not None:
					args = (descr,display_text,cols_offset,cols_label,repeating,repeating_table,required,wrap,filler,children,code,)
					self.db.executeSQLCommand(kUberGroupUpdateSQL, args)
				else:
					args = (code,descr,display_text,cols_offset,cols_label,repeating,repeating_table,required,wrap,filler,children,)
					self.db.executeSQLCommand(kUberGroupInsertSQL, args)

	def importRFP(self):
		fileData = self.getImportFileBySite("rfpQuestions.csv",kDelimiter)
		for row in fileData:
			if self.rowValid(row):
				identifier = row[0]
				if identifier == 'QUESTION':
					self.importQuestion(row)
				elif identifier == 'OPTION':
					self.importQuestionOption(row)

	def importQuestion(self,row):
		code = row[1]
		prompt = row[2]
		seqNbr = int(row[3].strip())
		required = self.getBooleanValue(row[4])
		active = self.getBooleanValue(row[5])
		identifier_code = row[6]
		nbr_rows= int(row[7].strip())
		task_code = row[8]
		tableKey = self.getTableKey("wf_question",code)
		if tableKey is not None:
			args = (task_code,prompt,required,seqNbr,active,identifier_code,nbr_rows,code,)
			self.db.executeSQLCommand(kQuestionUpdateSQL,args)
		else:
			args = (task_code,code,prompt,required,seqNbr,active,identifier_code,nbr_rows,)
			self.db.executeSQLCommand(kQuestionInsertSQL,args)

	def importQuestionOption(self,row):
		questionCode = row[1]
		code = row[2]
		optionText = row[3]
		hasText = self.getBooleanValue(row[4])
		textTitle = row[5]
		sequenceNbr = int(row[6].strip())
		textRequired = self.getBooleanValue(row[7])
		active = self.getBooleanValue(row[8])
		nbrRows = int(row[9].strip())
		questionid = self.getTableKey("wf_question",questionCode)
		tableKey = self.getTableKey("wf_question_option",code)
		if tableKey is not None:
			args = (questionid,optionText,hasText,textTitle,textRequired,sequenceNbr,active,nbrRows,code,)
			self.db.executeSQLCommand(kQuestionOptionUpdateSQL,args)
		else:
			args = (questionid,code,optionText,hasText,textTitle,textRequired,sequenceNbr,active,nbrRows,)
			self.db.executeSQLCommand(kQuestionOptionInsertSQL,args)

	def importMetaTracks(self):
		fileData = self.getImportFileBySite("metatrack.txt")
		for row in fileData:
			if self.rowValid(row):
				#Code|Description|Supplemental|Active|Tags
				code = row[0]
				descr = row[1]
				supplemental = stringUtils.interpretAsTrueFalse(row[2])
				active = stringUtils.interpretAsTrueFalse(row[3])
				tags = row[4]
				tableKey = self.getTableKey("wf_metatrack",code)
				if tableKey is not None:
					args = (descr,supplemental,active,tags,code)
					self.db.executeSQLCommand(kMetaTrackUpdateSQL,args)
				else:
					args = (code,descr,supplemental,active,tags)
					self.db.executeSQLCommand(kMetaTrackInsertSQL,args)

	def rowValid(self,row):
		if row == []:
			return False
		if row[0].startswith('#'):
			return False
		if row[0].strip() == '':
			return False
		return True


	def importTracks(self):
		fileData = self.getImportFileBySite("track.txt")
		for row in fileData:
			if self.rowValid(row):
				#Code|Description|MetatrackCode|Active|Tags
				code = row[0]
				descr = row[1]
				metatrackcode = row[2]
				trackId = self.getTableKey("wf_metatrack",metatrackcode)
				active = stringUtils.interpretAsTrueFalse(row[3])
				tags = row[4]
				tableKey = self.getTableKey("wf_track",code)
				if tableKey is not None:
					args = (descr,active,trackId,tags,code)
					self.db.executeSQLCommand(kTrackUpdateSQL,args)
				else:
					args = (code,descr,active,trackId,tags)
					self.db.executeSQLCommand(kTrackInsertSQL,args)

	def importTitles(self):
		#   Imports Titles "the old way":
		#       - smashes the TrackCode and TitleDescription together to obtain a unique TitleCode
		#       - JobCode has nothing to do with the price of fish
		fileData = self.getImportFileBySite("title.txt")
		for row in fileData:
			if self.rowValid(row):
				#JobCode|TrackCode|TitleDescription|PositionCriteria|Active|RankOrder|IsActionable|Tags
				jobcode	= row[0]
				trackcode = row[1]
				title = row[2]
				track_id = self.getTableKey('wf_track',trackcode)
				code = self.manufactureCode([trackcode,title])
				positioncriteria = row[3]
				active = stringUtils.interpretAsTrueFalse(row[4])
				rankorder = mpsMath.getIntFromString(row[5])
				isactionable = stringUtils.interpretAsTrueFalse(row[6])
				tags = row[7]
				tableKey = self.getTableKey("wf_title",code)
				if tableKey is not None:
					args = (title,active,jobcode,track_id,positioncriteria,rankorder,isactionable,tags,code,)
					self.db.executeSQLCommand(kTitleUpdateSQL,args)
				else:
					args = (code,title,active,jobcode,track_id,positioncriteria,rankorder,isactionable,tags)
					self.db.executeSQLCommand(kTitleInsertSQL,args)

	def importTitles2(self):
		#   Imports Titles "the new way":
		#       - matches the table definition with no hokey on-the-fly unique code manufacturization
		#       - each row has a unique TitleCode
		#       - TitleCode is used as the JobCode
		fileData = self.getImportFileBySite("title2.txt")
		for row in fileData:
			if self.rowValid(row):
				#TitleCode|TrackCode|TitleDescription|PositionCriteria|Active|RankOrder|IsActionable|Tags
				titlecode	= row[0]
				trackcode = row[1]
				track_id = self.getTableKey('wf_track',trackcode)
				descr = row[2]
				positioncriteria = row[3]
				active = stringUtils.interpretAsTrueFalse(row[4])
				rankorder = mpsMath.getIntFromString(row[5])
				isactionable = stringUtils.interpretAsTrueFalse(row[6])
				tags = row[7]
				jobcode = titlecode

				tableKey = self.getTableKey("wf_title",titlecode)
				if tableKey is not None:
					args = (descr,active,jobcode,track_id,positioncriteria,rankorder,isactionable,tags,titlecode)
					self.db.executeSQLCommand(kTitleUpdateSQL,args)
				else:
					args = (titlecode,descr,active,jobcode,track_id,positioncriteria,rankorder,isactionable,tags)
					self.db.executeSQLCommand(kTitleInsertSQL,args)

	def importDepartments(self):
		#   Imports Departments "the old way":
		#       - department addresses are in a single, pipe delimited field
		fileData = self.getImportFileBySite("department.txt",'\t')
		for row in fileData:
			if self.rowValid(row):
				#code	descr	parent_code	pcncode	ccacctcd	header_image	email_address	address_lines	address_suffix	city	state	postal
				code = row[0]
				descr = row[1]
				parent_code = row[2]
				parent_id = self.getTableKey("wf_department",parent_code)
				pcncode = row[3].rjust(2,'0')
				ccacctcd = row[4]
				header_image = row[5]
				email_address = row[6]
				address_lines = row[7]
				address_json = self.jsonify(address_lines)
				address_suffix = row[8]
				suffix_json = self.jsonify(address_suffix)
				city = row[9]
				state = row[10]
				postal = row[11]
				pcnKey = self.getTableKey("wf_pcn",pcncode)
				if pcnKey == None:
					self.createPCN(pcncode)
				pcnKey = self.getTableKey("wf_pcn",pcncode)
				tableKey = self.getTableKey("wf_department",code)
				if tableKey is not None:
					args = (descr,parent_id,pcnKey,ccacctcd,header_image,email_address,address_json,suffix_json,city,state,postal,code,)
					self.db.executeSQLCommand(kDepartmentUpdateSQL,args)
				else:
					args = (code,descr,parent_id,pcnKey,ccacctcd,header_image,email_address,address_json,suffix_json,city,state,postal,)
					self.db.executeSQLCommand(kDepartmentInsertSQL,args)

	def importDepartments2(self):
		#   Imports Departments "the new way":
		#       - pipe delimited
		#       - department addresses are in 5 separate columns and need to be strung together
		#       - no support for multiple lines in the address suffix field
		fileData = self.getImportFileBySite("department2.txt")
		for row in fileData:
			if self.rowValid(row):
				#DeptCode|Description|ParentCode|PCNPrefix|CCAcctCd|HeaderImage|EmailAddress|Address1|Address2|Address3|Address4|Address5|AddressSuffix|City|State|PostalCode
				code = row[0]
				descr = row[1]
				parent_code = row[2]
				pcncode = row[3].rjust(2,'0')
				ccacctcd = row[4]
				header_image = row[5]
				email_address = row[6]
				address1 = row[7]
				address2 = row[8]
				address3 = row[9]
				address4 = row[10]
				address5 = row[11]
				address_suffix = row[12]
				city = row[13]
				state = row[14]
				postal = row[15]

				parent_id = self.getTableKey("wf_department", parent_code)
				pcnKey = self.getTableKey("wf_pcn",pcncode)
				if pcnKey == None:
					self.createPCN(pcncode)
				pcnKey = self.getTableKey("wf_pcn",pcncode)

				addressLines = []
				if address1: addressLines.append(address1)
				if address2: addressLines.append(address2)
				if address3: addressLines.append(address3)
				if address4: addressLines.append(address4)
				if address5: addressLines.append(address5)
				address_json = json.dumps(addressLines)
				suffix_json = json.dumps([address_suffix])

				tableKey = self.getTableKey("wf_department",code)
				if tableKey is not None:
					args = (descr,parent_id,pcnKey,ccacctcd,header_image,email_address,address_json,suffix_json,city,state,postal,code,)
					self.db.executeSQLCommand(kDepartmentUpdateSQL,args)
				else:
					args = (code,descr,parent_id,pcnKey,ccacctcd,header_image,email_address,address_json,suffix_json,city,state,postal,)
					self.db.executeSQLCommand(kDepartmentInsertSQL,args)

	def createPCN(self,pcncode):
		sql = "INSERT INTO wf_pcn (code,seq) VALUES (%s,%s)"
		args = (pcncode,0,)
		self.db.executeSQLCommand(sql,args)

	def importDepartmentChairs(self):
		#   Imports Department Chairs "the old way":
		#       - chair titles are in a single, pipe delimited field
		fileData = self.getImportFileBySite("department_chair.txt")
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				department_id = self.getTableKey("wf_department",code)
				chair_with_degree = row[1]
				chair_titles = row[2]
				chair_signature = row[3]
				seq = mpsMath.getIntFromString(row[4],0)
				tableKey = self.getDepartmentChairTableKey(department_id,seq)
				if tableKey is not None:
					args = (chair_with_degree,chair_signature,chair_titles,department_id,seq,)
					self.db.executeSQLCommand(kDepartmentChairUpdateSQL,args)
				else:
					args = (department_id,chair_with_degree,chair_signature,chair_titles,seq,)
					self.db.executeSQLCommand(kDepartmentChairInsertSQL,args)

	def importDepartmentChairs2(self):
		#   Imports Department Chairs "the new way":
		#       - pipe delimited
		#       - chair titles are in 4 separate columns and need to be strung together
		#       - 2nd column is department name, which is ignored
		fileData = self.getImportFileBySite("department_chair2.txt")
		for row in fileData:
			if self.rowValid(row):
				#DeptCode|Description|ChairFullNameWithDegree|Title1|Title2|Title3|Title4|ChairSignature|Seq
				code = row[0]
				ignored = row[1]
				chair_with_degree = row[2]
				title1 = row[3]
				title2 = row[4]
				title3 = row[5]
				title4 = row[6]
				chair_signature = row[7]
				seq = mpsMath.getIntFromString(row[8],0)

				department_id = self.getTableKey("wf_department",code)
				titles = []
				if title1: titles.append(title1)
				if title2: titles.append(title2)
				if title3: titles.append(title3)
				if title4: titles.append(title4)
				chair_titles = '|'.join(titles)

				tableKey = self.getDepartmentChairTableKey(department_id,seq)
				if tableKey is not None:
					args = (chair_with_degree,chair_signature,chair_titles,department_id,seq,)
					self.db.executeSQLCommand(kDepartmentChairUpdateSQL,args)
				else:
					args = (department_id,chair_with_degree,chair_signature,chair_titles,seq,)
					self.db.executeSQLCommand(kDepartmentChairInsertSQL,args)

	def importPackets(self):
		fileData = self.getImportFileBySite("packets.txt")
		self.fullReplace()
		for row in fileData:
			if self.rowValid(row):
				rowIdentifier = row[0]
				if rowIdentifier == 'PACKET':
					self.upsertPacket(row)
				elif rowIdentifier == 'GROUP':
					self.upsertPacketGroup(row)
				elif rowIdentifier == 'ITEM':
					self.upsertPacketItem(row)

	def fullReplace(self):
		sql = "delete from wf_packet_item"
		self.db.executeSQLCommand(sql,())
		sql = "delete from wf_packet_group"
		self.db.executeSQLCommand(sql,())
		sql = "delete from wf_packet"
		self.db.executeSQLCommand(sql,())

	def upsertPacket(self,row):
		packetCode = row[1]
		packetDescr = row[2]
		tableKey = self.getTableKey("wf_packet",packetCode)
		if tableKey:
			self.db.executeSQLCommand(kPacketUpdateSQL,(packetDescr,packetCode,))
		else:
			self.db.executeSQLCommand(kPacketInsertSQL,(packetCode,packetDescr,))

	def upsertPacketGroup(self,row):
		packetCode = row[1]
		groupCode = row[2]
		groupDescr = row[3]
		seq = self.getPacketSeq(row[4])
		packetId = self.getTableKey("wf_packet",packetCode)
		whereClause = "code = '%s' and packet_id = %i" % (groupCode,packetId,)
		tableKey = self.getTableKeyForWhereClause("wf_packet_group",whereClause)
		if tableKey:
			self.db.executeSQLCommand(kPacketGroupUpdateSQL,(groupDescr,seq,groupCode,packetId))
		else:
			self.db.executeSQLCommand(kPacketGroupInsertSQL,(groupCode,groupDescr,seq,packetId,))

	def upsertPacketItem(self,row):
		#ITEM - group code, item code, sequence
		groupCode = row[1]
		itemCode = row[2]
		seq = self.getPacketSeq(row[3])
		isArtifact = self.getBooleanValue(row[4])
		artifactConfig = row[5]

		packetGroupId = self.getTableKey("wf_packet_group",groupCode)
		whereClause = "item_code = '%s' and packet_group_id = %i" % (itemCode,packetGroupId,)
		tableKey = self.getTableKeyForWhereClause("wf_packet_item",whereClause)
		if tableKey:
			self.db.executeSQLCommand(kPacketItemUpdateSQL,(seq,isArtifact,artifactConfig,itemCode,packetGroupId,))
		else:
			self.db.executeSQLCommand(kPacketItemInsertSQL,(itemCode,seq,packetGroupId,isArtifact,artifactConfig,))

	def getBooleanValue(self, value):
		if value:
			booleanValue = stringUtils.interpretAsTrueFalse(value)
			return booleanValue
		return False

	def getPacketSeq(self,strValue):
		returnVal = 1
		try:
			returnVal = int(strValue)
		except Exception,e:
			pass
		finally:
			return returnVal


	################## non site related ##################

	def importAppointmentStatuses(self):
		fileData = self.getImportFileBySite("appointment_status.txt")
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				tableKey = self.getTableKey("wf_appointment_status",code)
				if tableKey is not None:
					args = (descr,code,)
					self.db.executeSQLCommand(kAppointmentStatusUpdateSQL,args)
				else:
					args = (code,descr,)
					self.db.executeSQLCommand(kAppointmentStatusInsertSQL,args)


	def importComponentTypes(self):
		fileData = self.getImportFileBySite("component_type.txt")
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				tableKey = self.getTableKey("wf_component_type",code)
				if tableKey is not None:
					args = (descr,code,)
					self.db.executeSQLCommand(kComponentTypeUpdateSQL,args)
				else:
					args = (code,descr,)
					self.db.executeSQLCommand(kComponentTypeInsertSQL,args)

	def importJobActionTypes(self):
		fileData = self.getImportFileBySite("job_action_type.txt")
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				active = self.getBooleanValue(row[2])
				tableKey = self.getTableKey("wf_job_action_type",code)
				if tableKey is not None:
					args = (descr,active,code,)
					self.db.executeSQLCommand(kJobActionTypeUpdateSQL,args)
				else:
					args = (code,descr,active,)
					self.db.executeSQLCommand(kJobActionTypeInsertSQL,args)

	def importEvaluatorTypes(self):
		fileData = self.getImportFileBySite("evaluator_type.txt")
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				isExternal = self.getBooleanValue(row[2])
				isArmsLength = self.getBooleanValue(row[3])
				requiresApproval = self.getBooleanValue(row[4])
				tableKey = self.getTableKey("wf_evaluator_type",code)
				if tableKey is not None:
					args = (descr,isExternal,isArmsLength,requiresApproval,code,)
					self.db.executeSQLCommand(kEvaluatorTypeUpdateSQL,args)
				else:
					args = (code,descr,isExternal,isArmsLength,requiresApproval,)
					self.db.executeSQLCommand(kEvaluatorTypeInsertSQL,args)

	def importEvaluatorSources(self):
		fileData = self.getImportFileBySite("evaluator_source.txt")
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				tableKey = self.getTableKey("wf_evaluator_source",code)
				if tableKey is not None:
					args = (descr,code,)
					self.db.executeSQLCommand(kEvaluatorSourceUpdateSQL,args)
				else:
					args = (code,descr,)
					self.db.executeSQLCommand(kEvaluatorSourceInsertSQL,args)

	def importOracleTable(self):
		sql = "INSERT INTO oracle (data) values (%s)"
		facts = ["On or about 06/01/2015, Guido Gottasuiti was seen driving a 1994 maroon-colored Toyota Corolla",
			"The 1994 maroon-colored Toyota Corolla has a bumper sticker that says 'I brew the beer I drink'",
			"The 1994 maroon-colored Toyota Corolla is missing two hub caps, left front, left rear",
			"The Michigan license plate number is 4KT ***",
			"On, or about, July 8, 2015, Guido's 1994 Corolla was no longer parked at Guido's place of employment, however Guido was on site",
			"On August 6th, 2015, Guido's 1994 Corolla was spotted in a neighborhood in Northwest Ann Arbor (on the corner of Spring and Cherry)",
			"On August 26th, 2015, we started our walk at 9:47 AM. We encountered Glidewalker approximately 50 feet from his office door at 9:55 AM. We are moving the official start time to 9:48 AM to maximize encounter length.",
			"On August 27th, 2015, no Glidewalker. May be a fluke. Will maintain official start time at 9:48 AM",
			"On September 1, 2015, departed office at 9:55 AM with a quick bathroom stop by Luana. Halfway down the escalator, Glidewalker emerged from the tunnel. Experienced a full frontal stationary Glidewalker on the 2nd escalator. Wow!",
			"On September 1, 2015, observed Guido Gottasuiti exiting Building 200 for a smoke. Did not actually get to see The Man puffing on a cancer stick, though.",
			"As noted above, the last time we saw Guido's car was July 8, 2015. Today, September 15, 2015, it was back. Words cannot describe the emotional impact. It had been over 2 months and we'd all but given up hope. While the mystery is now ten-fold what it was before, the fact that it was there gives us hope for a brighter future, a better city, a greater state, a unified country and a healthy living, breathing planet.",
			"September 16.2015. Had a brief Glidewalker sighting. He was exiting the tunnel as we entered. Was able to catch a glimpse of him as he glided onto the escalator and floated to the first floor.",
			"September 22, 2015 at 10:24 AM. We walked by Guido's car. Approximately 74.5 yards from the car was Guido himself. He was having a smoke. He said 'GENTLEMEN! Nice morning for a walk!' We were left speechless.",
			"October 2, 2015 at 9:50 AM. Flying solo, EMP WFM, sick. Descending escalator to tunnel, saw Glidewalker rounding the curve and heading back west. Followed Glidey at distance of 30 ft all the way down the tunnel. Magical. Observed that Glidey is somewhat bow-legged. Determined that this contributes greatly to his unique stride, increasing his overall appeal.",
			"October 20, 2015 at 9:54:00 AM. A psychic premonition on Eric's part led to a Glidey/Guido double header on the typical morning hybrid. Spotted Glidey glide into the tunnel as well as Guido strutting and smoking in the MSIS parking lot. It was a grand experience with nearly indescribable physiological effects."
			"October 22, 2015 at 10:53 AM. Flying solo, Greg getting old, beaten-down, fridge fixed for  umpteenth time. Today was bring your family to work day at NCRC. Upon entering the tunnel, I saw Glidewalker and his entire family. This included his wife, 3 kids, an uncle, his parents and grandparents. Collectively, they floated through the tunnel like a butter on a warm griddle. I was amazed at each of them individually, as well as collectively. Most amazing to me was his two-year old son who maintained a straight posture, had his thumbs up, an exhibited virtually no vertical movement while keeping pace with the group. Later, when crossing Eisenhower Parkway, Smokey Bearette was on the corner with her family. Unfortunately, they were all dead. While rounding the corner by MSIS, there was Guido and his 2 sons ages 2, 4 as well as his daughter age 7. They were all dressed in suits, and were smoking unfiltered cigarettes. When they saw me, they all turned and shouted in unison 'GENTLEMAN!!! Nice morning for a walk!'"
			"Tuesday, November 17 on lunchtime walk. Saw Glidey in the wild, Smokey on the side and Guido showing pride.",
			'''On Monday, January 4, 2016, our first day back from Christmas break, we were boarding the escalator heading down into the tunnel. We heard a repeated, loud banging behind us. Greg turned around and, to his surprise, saw Guido a mere two steps behind him. This was our first close up encounter with the man himself. We could clearly hear his Australian accent as he commented that he would "need to tippie toe" in order to reduce the sounds of his stylish, hard-soled, boots. His suit was dark, clean and neatly pressed. We watched in awe as he seamlessly navigated his way through the tunnel.''',
			]

		for fact in facts:
			args = (fact,)
			self.db.executeSQLCommand(sql,args)

	def importTerminationType(self):
		fileData = self.getImportFileBySite("termination_types.txt")
		for row in fileData:
			if self.rowValid(row):
				code = row[0]
				descr = row[1]
				tableKey = self.getTableKey("wf_termination_type",code)
				if tableKey is not None:
					args = (descr,code,)
					self.db.executeSQLCommand(kTerminationTypeUpdateSQL,args)
				else:
					args = (code,descr,)
					self.db.executeSQLCommand(kTerminationTypeInsertSQL,args)

	def jsonify(self,pipedString):
		aList = []
		splits = pipedString.split(kDelimiter)
		for each in splits:
			if each:
				aList.append(each)
		return json.dumps(aList)

	def manufactureCode(self,stringList):
		code = ''
		for each in stringList:
			code += each.replace(' ','')
		return code

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)

	def getDepartmentChairTableKey(self,department_id,seq):
		sql = "SELECT id FROM wf_department_chair WHERE department_id = %s and seq = %s"
		args = (department_id,seq,)
		qry = self.db.executeSQLQuery(sql,args)
		if len(qry) > 0:
			return qry[0]['id']

	def getTableKey(self,tableName,code,lookupfield = 'code'):
		sql = "select id from %s where %s = '%s'" % (tableName,lookupfield,code)
		qry = self.db.executeSQLQuery(sql,())
		if len(qry) > 0:
			return qry[0]['id']

	def getTableKeyForWhereClause(self,tableName,whereClause = ''):
		sql = "select id from %s where %s" % (tableName, whereClause)
		qry = self.db.executeSQLQuery(sql,())
		if len(qry) > 0:
			return qry[0]['id']

	def getImportFileBySite(self, fileName, delimit = kDelimiter):
		data = []
		rute = os.path.abspath(__file__).split("car")[0]
		mySite = self.site.replace('.','_').replace('-','_')
		try:
			filepath = os.path.join(rute, 'car', 'data', 'atramData', 'sites', mySite, fileName)
			if not os.path.exists(filepath):
				filepath = os.path.join(rute, 'car', 'data', 'atramData', 'common', fileName)

			f = open(filepath, 'rU')
			data = list(csv.reader(f, delimiter=delimit))
			f.close()
			return data
		except:
			print "unable read file %s" % (fileName)
			pass
		finally:
			return data


class DataLoadInterface:
	DESCR = '''Data Load for Atram. Currently loads only lookup data.'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='dev', help='database name (default=dev')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-s', '--site', dest='site', default='dev', help='data for this site is loaded from /data/atramData/sites/{sitename}')
		parser.add_option('-x', '--destroy', dest='destroy', default="0", help='destroy existing data. 1=on, 0=off')
		parser.add_option('-o', '--optiononly', dest='optiononly', default="", help='import this item only - options: packet, rfp, or uber')

		return parser

	def run(self, options, args):
		atramLoad = None
		try:
			atramLoad = AtramLoad(options, args)
			atramLoad.process()
		except Exception, e:
			print e.message
		finally:
			if atramLoad:
				atramLoad.shutdown()


if __name__ == '__main__':
	logging.config.fileConfig(cStringIO.StringIO(MPSCore.core.constants.kDebugFormatFile))
	import MPSCore.utilities.sqlUtilities as sqlUtilities
	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
	sys.exit(0)
