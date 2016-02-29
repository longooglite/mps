# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''

'''

import codecs
import datetime
import optparse
import os
import os.path
import sys
import string
from os.path import expanduser
import collections
import MySQLdb as mysqldb



METATRACK_SQL = '''INSERT INTO METATRACK (NAME,ACTIVE) VALUES (%s,%s)'''
TRACK_EXISTS_SQL = '''SELECT ID FROM TRACK WHERE NAME = %s'''
TRACK_INSERT_SQL = '''INSERT INTO TRACK (NAME,ACTIVE,METATRACK_ID) VALUES (%s,%s,%s)'''
DEPARTMENT_SQL = '''SELECT ID FROM DEPARTMENT WHERE DEPTID = %s'''
PCN_SQL = '''INSERT INTO PCN_CODE (ID,PCN) VALUES (%s,%s)'''
PCN_EXISTS_SQL = '''SELECT ID FROM PCN_CODE WHERE ID = %s '''
DEPARTMENT_INSERT_SQL = '''INSERT INTO DEPARTMENT (NAME,DEPTID,PARENT_ID,PCN_CODE,CHILD_INDEX,CC_ACCT_CD) VALUES (%s,%s,%s,%s,null,0)'''
DEPARTMENT_INFO_INSERT_SQL = '''INSERT INTO DEPARTMENT_INFO (CHAIR_WITH_DEGREE,CHAIR_TITLES,ADDRESS,DEPTID,EMAIL_ADDRESS) VALUES (%s,%s,%s,%s,%s)'''
TITLE_INSERT_SQL = '''INSERT INTO TITLE (NAME,ACTIVE,JOBCODE,TRACK_ID,NEW_APPT,PROMOTION,CRITERIA_ID,RANK_ORDER) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
PROSPECT_SQL = '''INSERT INTO prospect (LOGIN_ID,EMAIL,FIRST_NAME,LAST_NAME,APPT_REQ) VALUES (%s,%s,%s,%s,1)'''
FACULTY_SQL = '''INSERT INTO faculty (ID) VALUES (%s)'''
POSITION_SQL = '''INSERT INTO position (DTYPE,DEPARTMENT_ID,METATRACK_ID,PROPOSED_TITLE_ID,PCN,STATUS) VALUES (%s,%s,%s,%s,%s,'FILLED')'''
POSITION_LIST_ITEM_SQL = '''INSERT INTO position_list_item (ID,PCN,NAME,STATUS,STATUS_SORT,DEPARTMENT_ID,TITLE_ID,JA_ID,FACULTY_ID,P_STATE,SECONDARY,ACTION_DATE) VALUES (%s,%s,%s,'FILLED',700,%s,%s,0,%s,'Filled',%s,%s)'''
APPOINTMENT_SQL = '''INSERT INTO appointment (POSITION_ID,TITLE_ID,FACULTY_ID,STATUS,START_DATE) VALUES (%s,%s,%s,'FILLED',%s)'''
JOB_ACTION_SQL = '''INSERT INTO job_action (APPT_ID,POSITION_ID,STATUS,ARCHIVED_DATE,ARCHIVED_REASON) VALUES (%s,%s,'APPROVED',%s,'Completed')'''
NEW_APPT_JOB_ACTION_SQL = '''INSERT INTO new_appt_job_action (ID) VALUES (%s)'''
USERS_SQL = '''INSERT INTO users (USERNAME,PASSWORD) VALUES (%s,'PASSWORD')'''
AUTHORITIES_SQL = '''INSERT INTO authorities (USERNAME,AUTHORITY) VALUES (%s,'ROLE_CANDIDATE')'''
UPDATE_PCN_SQL = '''UPDATE pcn_code SET pcn=%s WHERE id=%s'''

### Column Headers ###
kDEPT_ID = 'DEPT_ID'
kDEPT_NAME = 'Name'
kDEPT_ADDRESS1 = 'Dept Address 1'
kDEPT_ADDRESS2 = 'Dept Address 2'
kDEPT_ADDRESS3 = 'Dept Address 3'
kDEPT_CITY = 'Dept City'
kDEPT_STATE = 'Dept State'
kDEPT_ZIP = 'Dept Zip'
kDEPT_CHAIR_NAME = 'Dept Chair Full Name with Degree'
kDEPT_CHAIR_TITLE1 = 'Dept Chair title 1'
kDEPT_CHAIR_TITLE2 = 'Dept Chair title 2'
kDEPT_CHAIR_TITLE3 = 'Dept Chair title 3'
kDEPT_CHAIR_TITLE4 = 'Dept Chair title 4'
kDEPT_EMAIL = 'Email'

kPARENT_DEPT_ID = 'PARENT_ID'
kPCN_CODE = 'PCN'
kEMAIL = "Email"
kTRACK = "Track"
kTITLE = "Title"
kJOB_CODE = "Job_Code"
kRANKORDER = "Rank_Order"

schoolPaths = {"CMU":"/CAR/trunk/car/MartaLegacy/sites/CMU/DataLoad/"}

class DataLoad(object):
	# Initialization

	def __init__(self, options=None, args=None):
		self.srcPath = expanduser("~") + schoolPaths.get(options.school,"CMU")
		self.host = "localhost"
		self.port = 3306
		self.dbname = 'marta'
		self.user = 'marta'
		self.password = 'atram'

		self.db = None
		self.deptCache = collections.OrderedDict()
		self.titleCache = {}
		self.trackCache = {}
		self.rosterCache = {}
		self.messageList = []

		self.startDate = datetime.date(2012, 4, 1)
		self.actionDate = datetime.datetime(2012, 4, 1)
		self.today = datetime.date.today()
		self.includeConsoleLog = True

		self.nbrIgnored = 0
		self.nbrProcessed = 0
		self.nbrErrors = 0

		self.host = options.host
		self.port = int(options.port)
		self.dbname = options.dbname
		self.user = options.user
		self.password = options.password
		self.destroy = options.destroy

		self.logSetup()


	#	Shutdown

	def shutdown(self):
		pass


	#	Execution

	def process(self):
		try:
			self.logProcessStart()
			self.connectToDatabase()

			self.processSourceFolder()

			self.logStats()
			self.logProcessEnd()
		finally:
			pass


	def processSourceFolder(self):

		self.destroy = '1'

		if self.destroy == '1':
			self.executeStatement('delete from new_appt_job_action;',None)
			self.executeStatement('delete from promotion_job_action;',None)
			self.executeStatement('delete from job_action_evaluators;',None)
			self.executeStatement('delete from ja_evaluations_items;',None)
			self.executeStatement('delete from ja_document_items;',None)
			self.executeStatement('delete from ja_item;',None)
			self.executeStatement('delete from job_action;',None)
			self.executeStatement('delete from appointment;',None)
			self.executeStatement('delete from position_list_item;',None)
			self.executeStatement('delete from position;',None)
			self.executeStatement('delete from faculty;',None)
			self.executeStatement('delete from prospect;',None)
			self.executeStatement('update department set parent_id = null;',None)
			self.executeStatement('delete from department;',None)
			self.executeStatement('delete from department_info;',None)
			self.executeStatement('delete from pcn_code;',None)
			self.executeStatement('delete from packet_approvals;',None)
			self.executeStatement('delete from title;',None)
			self.executeStatement('delete from track;',None)
			self.executeStatement('delete from metatrack;',None)
			self.executeStatement("DELETE FROM GROUP_MEMBERS;",None)
			self.executeStatement("DELETE FROM AUTHORITIES;",None)
			self.executeStatement("DELETE FROM users;",None)

		self.logMessage("Processing source folder")
		departmentsFile = None
		titlesFile = None
		rosterFile = None
		try:
			departmentsFile = self.loadFile('departments.txt')
			self.cacheDepartments(departmentsFile)
			titlesFile = self.loadFile('titles.txt')
			self.cacheTitles(titlesFile)
			self.processDepartmentCache()
			self.processTitleCache()
		finally:
			try:
				self.closeSourceFiles([departmentsFile,titlesFile,rosterFile])
			except Exception, e:
				pass

	def processDepartmentCache(self):
		try:
			for parentKey in self.deptCache:
				department = self.deptCache[parentKey]
				existingParentId = self.executeQuery("SELECT ID FROM DEPARTMENT WHERE DEPTID = '%s'" % (department[kPARENT_DEPT_ID]),None)
				parentId = None
				if len(existingParentId) > 0:
					parentId = existingParentId[0]['ID']
				pcnCodeId = self.pcnCodeExists(department[kPCN_CODE],)
				if pcnCodeId is None:
					pcnCodeId = 0 if department[kPCN_CODE] == '' else int(department[kPCN_CODE])
					args = (pcnCodeId,1)
					self.executeStatement(PCN_SQL,args)
				args = (department[kDEPT_NAME], department[kDEPT_ID], parentId, pcnCodeId)
				self.executeInsertReturnId(DEPARTMENT_INSERT_SQL,args)
				address = self.getDeptAddress(department)
				chairNameDegree = self.getDeptChairName(department)
				chairTitle = self.getDeptChairTitle(department)
				email = self.getDeptEmail(department)
				args = (chairNameDegree,chairTitle,address,department[kDEPT_ID],email,)
				self.executeInsertReturnId(DEPARTMENT_INFO_INSERT_SQL,args);
		except Exception,e:
			pass

	def getDeptEmail(self,department):
		return department.get(kDEPT_EMAIL,'')

	def getDeptAddress(self,department):
		returnVal = department.get(kDEPT_ADDRESS1,'')
		address2 = department.get(kDEPT_ADDRESS2,'')
		if address2:
			returnVal += "<br/>%s" % (address2)
		address3 = department.get(kDEPT_ADDRESS3,'')
		if address3:
			returnVal += "<br/>%s" % (address3)
		city = department.get(kDEPT_CITY,'')
		state = department.get(kDEPT_STATE,'')
		zip = department.get(kDEPT_ZIP,'')
		returnVal += "<br/>%s, %s %s" % (city,state,zip)
		return returnVal

	def getDeptChairName(self,department):
		return department.get(kDEPT_CHAIR_NAME,'')

	def getDeptChairTitle(self,department):
		chair1 = department.get(kDEPT_CHAIR_TITLE1,'')
		chair2 = department.get(kDEPT_CHAIR_TITLE2,'')
		chair3 = department.get(kDEPT_CHAIR_TITLE3,'')
		chair4 = department.get(kDEPT_CHAIR_TITLE4,'')
		returnVal = chair1
		if chair2:
			returnVal += "<br/>%s" % (chair2)
		if chair3:
			returnVal += "<br/>%s" % (chair3)
		if chair4:
			returnVal += "<br/>%s" % (chair4)
		return returnVal

	def processTitleCache(self):
		metaTrackId = self.createMetaTrack('Dummy',0)
		dummyTrackId = self.createTrack('Dummy', metaTrackId,0)
		self.createTitle(dummyTrackId,0)

		for key in self.titleCache:
			title = self.titleCache[key]

			args = (title[kTRACK],1,metaTrackId,)
			trackId = self.trackExists(title[kTRACK])
			if trackId is None:
				trackId = self.executeInsertReturnId(TRACK_INSERT_SQL,args)
			args = (title[kTITLE],1,title[kJOB_CODE],trackId,1,1,None,title[kRANKORDER],)
			self.executeInsertReturnId(TITLE_INSERT_SQL,args)

	def trackExists(self,name):
		value = self.executeQuery(TRACK_EXISTS_SQL,(name,))
		return None if len(value) == 0 else value[0]['ID']

	def pcnCodeExists(self,pcnCode):
		value = self.executeQuery(PCN_EXISTS_SQL,(pcnCode,))
		return None if len(value) == 0 else value[0]['ID']


	def createMetaTrack(self,name,active = 1):
		value = self.executeInsertReturnId(METATRACK_SQL,(name,active))
		return value if type(value) is long else None

	def createTrack(self,name,metaTrackId,active = 1):
		value = self.executeInsertReturnId(TRACK_INSERT_SQL,(name,active,metaTrackId))
		return value if type(value) is long else None

	def createTitle(self,trackId,active):
		dummy = '''INSERT INTO TITLE (ID,NAME,ACTIVE,JOBCODE,TRACK_ID,NEW_APPT,PROMOTION,CRITERIA_ID,RANK_ORDER) VALUES (1,'Dummy',%s,'000000',%s,1,1,null,0)'''
		self.executeStatement(dummy, (active,trackId,))

	def cacheTitles(self,file):
		isHeader = True
		for rawline in file:
			line = self.getLine(rawline)
			if isHeader:
				header = self.getHeader(line)
				isHeader = False
			else:
				jobCode = line[header[kJOB_CODE]]
				if not self.titleCache.has_key(jobCode):
					self.titleCache[jobCode] = self.getTitleDict(header,line)
				else:
					self.logMessage("Title file contains duplicate job code: %s. Only one will be persisted." % (jobCode))


	def cacheDepartments(self,departmentsFile):
		isHeader = True

		for rawline in departmentsFile:
			line = self.getLine(rawline)
			if isHeader:
				header = self.getHeader(line)
				isHeader = False
			else:
				departmentId = line[header[kDEPT_ID]]
				if not self.deptCache.has_key(departmentId):
					self.deptCache[departmentId] = self.getDepartmentDict(header,line)
				else:
					self.logMessage("Department file contains duplicate department ids: %s. Only one will be persisted." % (departmentId))


	def getColumnValue(self,line,header,key):
		returnVal = ''
		try:
			returnVal = line[header[key]].strip()
		except:
			pass
		return returnVal


	def getTitleDict(self,header,line):
		returnVal = {}
		returnVal[kJOB_CODE] = self.getColumnValue(line,header,kJOB_CODE)
		returnVal[kTITLE] = self.getColumnValue(line,header,kTITLE)
		returnVal[kTRACK] = self.getColumnValue(line,header,kTRACK)
		returnVal[kRANKORDER] = self.getColumnValue(line,header,kRANKORDER)
		return returnVal

	def getDepartmentDict(self,header,line):
		ampersandEscape = '&#038;'
		returnVal = {}
		returnVal[kDEPT_ID] = self.getColumnValue(line,header,kDEPT_ID)
		name = self.getColumnValue(line,header,kDEPT_NAME)
		returnVal[kDEPT_NAME] = string.replace(name,'&',ampersandEscape)
		returnVal[kPARENT_DEPT_ID] = self.getColumnValue(line,header,kPARENT_DEPT_ID)
		returnVal[kPCN_CODE] = self.getColumnValue(line,header,kPCN_CODE)
		returnVal[kEMAIL] = self.getColumnValue(line,header,kEMAIL)
		returnVal[kDEPT_ADDRESS1] = self.getColumnValue(line,header,kDEPT_ADDRESS1)
		returnVal[kDEPT_ADDRESS2] = self.getColumnValue(line,header,kDEPT_ADDRESS2)
		returnVal[kDEPT_ADDRESS3] = self.getColumnValue(line,header,kDEPT_ADDRESS3)
		returnVal[kDEPT_CITY] = self.getColumnValue(line,header,kDEPT_CITY)
		returnVal[kDEPT_STATE] = self.getColumnValue(line,header,kDEPT_STATE)
		returnVal[kDEPT_ZIP] = self.getColumnValue(line,header,kDEPT_ZIP)
		returnVal[kDEPT_CHAIR_NAME] = self.getColumnValue(line,header,kDEPT_CHAIR_NAME)
		returnVal[kDEPT_CHAIR_TITLE1] = self.getColumnValue(line,header,kDEPT_CHAIR_TITLE1)
		returnVal[kDEPT_CHAIR_TITLE2] = self.getColumnValue(line,header,kDEPT_CHAIR_TITLE2)
		returnVal[kDEPT_CHAIR_TITLE3] = self.getColumnValue(line,header,kDEPT_CHAIR_TITLE3)
		returnVal[kDEPT_CHAIR_TITLE4] = self.getColumnValue(line,header,kDEPT_CHAIR_TITLE4)

		returnVal['children'] = {}
		return returnVal


	def getHeader(self,header):
		indexes = {}
		counter = 0
		for each in header:
			indexes[each.strip()] = counter
			counter = counter + 1
		return indexes

	def loadFile(self,fileName):
		print "Loading %s" % (fileName)
		file = None
		try:
			file = codecs.open(self.srcPath + fileName, 'r', 'utf-8', errors='ignore')
		except Exception, e:
			self.logMessage("Unable to open %s error %s" % (fileName,e.args))
			sys.exit(1)
		return file


	def processTitles(self,titlesFile):
		for rawline in titlesFile:
			line = self.getLine(rawline)
			print line


	def getLine(self,line):
		splits = line.split("\t")
		return splits


	def closeSourceFiles(self,srcFiles):
		try:
			for f in srcFiles:
				if f <> None:
					f.close()
		except:
			pass


	#	Database

	def getCursor(self):
		return self.db.cursor(mysqldb.cursors.DictCursor)

	def executeStatement(self, _stmt, _args=None):
		curs = None
		try:
			curs = self.getCursor()
			curs.execute(_stmt, _args)
			self.db.commit()
		finally:
			if curs:
				curs.close()

	def executeQuery(self, _query, _args=None):
		curs = None
		try:
			curs = self.getCursor()
			curs.execute(_query, _args)
			results = curs.fetchall()
			self.db.rollback()
			return results
		except Exception,e:
			pass
		finally:
			if curs:
				curs.close()

	def executeInsertReturnId(self, _stmt, _args=None):
		curs = None
		try:
			curs = self.getCursor()
			curs.execute(_stmt, _args)
			self.db.commit()
			curs.execute("SELECT LAST_INSERT_ID() AS ID")
			return curs.fetchone()['ID']
		except Exception,e:
			pass
		finally:
			if curs:
				curs.close()


	#	Logging

	def logSetup(self):
		if self.includeConsoleLog:
			print "%s Data Load processor created" % (self.getLogTimestamp())
			print "%s - Source: %s" % (self.getLogTimestamp(), self.srcPath)
			print "%s - Host: %s" % (self.getLogTimestamp(), self.host)
			print "%s - Port: %s" % (self.getLogTimestamp(), str(self.port))
			print "%s - Dbname: %s" % (self.getLogTimestamp(), self.dbname)
			print "%s - User: %s" % (self.getLogTimestamp(), self.user)
			print "%s - Password: %s" % (self.getLogTimestamp(), self.password)

	def logProcessStart(self):
		if self.includeConsoleLog:
			self.processStart = self.getLogTimestamp()
			print "%s Roster Load process started" % (self.processStart)

	def logStats(self):
		if self.includeConsoleLog:
			self.logMessage("")
			self.logMessage("%s Input lines read" % str(self.nbrIgnored + self.nbrProcessed))
			self.logMessage("%s Input lines ignored" % str(self.nbrIgnored))
			self.logMessage("%s Input lines processed" % str(self.nbrProcessed))
			self.logMessage("%s Input lines had errors" % str(self.nbrErrors))

	def logProcessEnd(self):
		if self.includeConsoleLog:
			self.processEnd = self.getLogTimestamp()
			self.logMessage("")
			print "%s Roster Load process completed" % (self.processEnd)
			print "%s Roster Load elapsed time: %s" % (self.processEnd, str(self.processEnd - self.processStart))

	def logMessage(self, _message):
		if self.includeConsoleLog:
			if _message:
				print "%s - %s" % (self.getLogTimestamp(), _message)
			else:
				print "%s" % (self.getLogTimestamp(),)

	def getLogTimestamp(self):
		return datetime.datetime.now()


	#	Internal Data class.


	def connectToDatabase(self):
		self.logMessage("Establishing database connection")
		self.db = mysqldb.connect(host=self.host, port=self.port, db=self.dbname, user=self.user, passwd=self.password)

class DataLoadInterface:
	DESCR = '''DataLoad is a powerful utility that reads CSV files and imports data into Marta. Good luck Jim.'''

	def __init__(self):
		pass

	def get_parser(self):

		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-s', '--school', dest='school', default="CMU", help='school name')
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=3306, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='marta', help='database name (default=marta')
		parser.add_option('-u', '--user', dest='user', default='marta', help='database user (default=marta)')
		parser.add_option('-w', '--password', dest='password', default='atram', help='database password')
		parser.add_option('-x', '--destroy', dest='destroy', default='atram', help='database password')

		return parser


	def run(self, options, args):
		try:
			dataLoad = DataLoad(options, args)
			dataLoad.process()
		except Exception, e:
			for each in e.args:
				print each
		finally:
			if dataLoad:
				dataLoad.shutdown()


if __name__ == '__main__':
	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
