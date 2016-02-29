# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
roster.py

Roster is an uncheesy little script to load Faculty into the MARTA Roster.

Usage:

$ python /path/to/roster.py -i /path/to/tab/delimited/file.csv

'''

import codecs
import datetime
import optparse
import os
import os.path
import datetime
import sys
import MySQLdb as mysqldb
from os.path import expanduser

schoolPaths = {"CMU":"/CAR/trunk/car/MartaLegacy/sites/CMU/DataLoad/"}

#column headers

kJOB_CODE = "JOB_CODE"
kGLOBAL_ID = 'GLOBAL_ID'
kEMAIL_ADDRESS = 'EMAIL_ADDRESS'
kFIRST_NAME = 'FIRST_NAME'
kLAST_NAME = 'LAST_NAME'
kMIDDLE_INITIAL = 'MIDDLE_INITIAL'
kSUFFIX = 'SUFFIX'
kNPI = 'NPI'
kAPPOINTMENT_TYPE = 'APPOINTMENT_TYPE'
kDATE_OF_BIRTH = 'DATE_OF_BIRTH'
kGENDER = 'GENDER'
kBIRTH_COUNTRY = 'BIRTH_COUNTRY'
kBIRTH_STATE = 'BIRTH_STATE'
kUS_CITIZEN = 'US Citizen'
kLIVING_IN_US = 'LIVING_IN_US'
kHAS_SSN = 'HAS_SSN'
kETHNICITY = 'ETHNICITY'
kSCHOLARLY_FOCUS = 'SCHOLARLY_FOCUS'
kALIASES = 'ALIASES'
kLANGUAGES = 'LANGUAGES'
kADDRESS_LINE1 = 'ADDRESS_LINE1'
kADDRESS_LINE2 = 'ADDRESS_LINE2'
kADDRESS_LINE3 = 'ADDRESS_LINE3'
kADDRESS_LINE4 = 'ADDRESS_LINE4'
kADDRESS_CITY = 'ADDRESS_CITY'
kADDRESS_STATE = 'ADDRESS_STATE'
kADDRESS_COUNTRY = 'ADDRESS_COUNTRY'
kADDRESS_ZIP = 'ADDRESS_ZIP'
kADDRESS_PHONE = 'ADDRESS_PHONE'
kADDRESS_FAX = 'ADDRESS_FAX'
kHD_PROGRAM = 'HD_PROGRAM'
kHD_DEGREE = 'HD_DEGREE'
kHD_INSTITUTION = 'HD_INSTITUTION'
kHD_COUNTRY = 'HD_COUNTRY'
kHD_STATE = 'HD_STATE'
kHD_CITY = 'HD_CITY'
kHD_NAME = 'HD_NAME'
kHD_START = 'HD_START'
kHD_END = 'HD_END'
kDEPT_ID = 'DEPARTMENT_ID'
kAPPT_START = 'DATE_OF_APPT'
kEASTYWESTY = 'LOCATION'


DEPARTMENT_SQL = '''SELECT * FROM DEPARTMENT'''
TITLE_SQL = '''SELECT * FROM TITLE WHERE ACTIVE = 1'''
TRACK_SQL = '''SELECT * FROM TRACK'''
PCN_SQL = '''SELECT * FROM PCN_CODE'''
PROSPECT_SQL = '''INSERT INTO prospect (LOGIN_ID,EMAIL,FIRST_NAME,LAST_NAME,APPT_REQ,NPI) VALUES (%s,%s,%s,%s,1,%s)'''
FACULTY_SQL = '''INSERT INTO faculty (ID) VALUES (%s)'''
POSITION_SQL = '''INSERT INTO position (DTYPE,DEPARTMENT_ID,METATRACK_ID,PROPOSED_TITLE_ID,PCN,STATUS) VALUES (%s,%s,%s,%s,%s,'FILLED')'''
POSITION_LIST_ITEM_SQL = '''INSERT INTO position_list_item (ID,PCN,NAME,STATUS,STATUS_SORT,DEPARTMENT_ID,TITLE_ID,JA_ID,FACULTY_ID,P_STATE,SECONDARY,ACTION_DATE) VALUES (%s,%s,%s,'FILLED',700,%s,%s,0,%s,'Filled',%s,%s)'''
APPOINTMENT_SQL = '''INSERT INTO appointment (POSITION_ID,TITLE_ID,FACULTY_ID,STATUS,START_DATE) VALUES (%s,%s,%s,'FILLED',%s)'''
JOB_ACTION_SQL = '''INSERT INTO job_action (APPT_ID,POSITION_ID,STATUS,ARCHIVED_DATE,ARCHIVED_REASON,ARCHIVED) VALUES (%s,%s,'APPROVED',%s,'Completed',1)'''
NEW_APPT_JOB_ACTION_SQL = '''INSERT INTO new_appt_job_action (ID) VALUES (%s)'''
USERS_SQL = '''INSERT INTO users (USERNAME,PASSWORD) VALUES (%s,'PASSWORD')'''
AUTHORITIES_SQL = '''INSERT INTO authorities (USERNAME,AUTHORITY) VALUES (%s,'ROLE_CANDIDATE')'''
UPDATE_PCN_SQL = '''UPDATE pcn_code SET pcn=%s WHERE id=%s'''
PERSONAL_INFO_SQL = '''INSERT INTO PERSONAL_INFO (ID,DOB,BIRTH_COUNTRY,BIRTH_STATE,GENDER,US_CITIZEN,LIVING_IN_US,HAS_SSN,ETHNICITY,SCHOLARLY_FOCUS,
ALIASES,LANGUAGES,ADDRESS_LINE1,ADDRESS_LINE2,ADDRESS_LINE3,ADDRESS_LINE4,ADDRESS_CITY,ADDRESS_STATE,ADDRESS_COUNTRY,ADDRESS_ZIP,ADDRESS_PHONE,
ADDRESS_FAX,HD_PROGRAM,HD_DEGREE,HD_INSTITUTION,HD_COUNTRY,HD_STATE,HD_CITY,HD_NAME,HD_START,HD_END,COMPLETED_DATE)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

class Roster(object):

	#	Initialization

	def __init__(self, options=None, args=None):
		self.srcPath = expanduser("~") + schoolPaths.get(options.school,"CMU") + "roster.txt"
		self.host = "localhost"
		self.port = 3306
		self.dbname = 'marta'
		self.user = 'marta'
		self.password = 'atram'

		self.db = None
		self.deptCache = {}
		self.titleCache = {}
		self.trackCache = {}
		self.pcnCache = {}
		self.messageList = []
		self.fileHeader = {}

		self.startDate = datetime.date(2012,4,1)
		self.actionDate = datetime.datetime(2012,4,1)
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

		self.logSetup()


	#	Shutdown

	def shutdown(self):
		pass


	#	Execution

	def process(self):
		try:
			self.logProcessStart()

			self.connectToDatabase()
			self.cacheDepartmentsByCode()
			self.cacheTitlesByJobCode()
			self.cacheTracksById()
			self.cachePcnById()

			self.processSourceFile()
			self.savePcns()

			self.logStats()
			self.logProcessEnd()
		finally:
			pass

	def connectToDatabase(self):
		self.logMessage("Establishing database connection")
		self.db = mysqldb.connect(host=self.host, port=self.port, db=self.dbname, user=self.user, passwd=self.password)

	def cacheDepartmentsByCode(self):
		self.logMessage("Caching Departments")
		departments = self.executeQuery(DEPARTMENT_SQL);
		for thisDept in departments:
			self.deptCache[thisDept['DEPTID']] = thisDept
		self.logMessage("  %i Departments loaded" % len(self.deptCache))

	def cacheTitlesByJobCode(self):
		self.logMessage("Caching Titles")
		titles = self.executeQuery(TITLE_SQL);
		for thisTitle in titles:
			self.titleCache[thisTitle['JOBCODE']] = thisTitle
		self.logMessage("  %i Titles loaded" % len(self.titleCache))

	def cacheTracksById(self):
		self.logMessage("Caching Tracks")
		tracks = self.executeQuery(TRACK_SQL);
		for thisTrack in tracks:
			self.trackCache[thisTrack['ID']] = thisTrack
		self.logMessage("  %i Tracks loaded" % len(self.trackCache))

	def cachePcnById(self):
		self.logMessage("Caching PCNs")
		self.pcnCache[0L] = {'ID': 0L, 'PCN': 0L }
		pcns = self.executeQuery(PCN_SQL);
		for thisPcn in pcns:
			self.pcnCache[thisPcn['ID']] = thisPcn
		self.logMessage("  %i PCNs loaded" % len(self.pcnCache))

	def processSourceFile(self):
		self.logMessage("Processing source file")
		srcFile = None
		try:
			srcFile = codecs.open(self.srcPath, 'r', 'utf-8', errors='ignore')
			processedHeader = False
			for line in srcFile:
				if len(line.strip()) == 0:
					continue
				splits = line.split("\t")
				if not processedHeader:
					processedHeader = True
					self.nbrIgnored += 1
					self.fileHeader = self.getFileHeader(splits)
				else:
					if len(splits) < len(self.fileHeader):
						self.nbrIgnored += 1
					else:
						self.processOneLine(Roster.InData(splits,self.fileHeader))

		finally:
			if srcFile is not None:
				try: srcFile.close()
				except Exception, e: pass

	def getFileHeader(self,header):
		indexes = {}
		counter = 0
		for each in header:
			indexes[each.strip()] = counter
			counter = counter + 1
		return indexes


	def processOneLine(self, _inData):
		if len(_inData.inLogin.strip()) == 0:
			return
		self.nbrProcessed += 1
		self.messageList = []
		self.resolveDepartment(_inData)
		self.resolveJobCode(_inData)
		self.resolveMetatrack(_inData)

		if _inData.eastywesty.strip():
			facultyId = self.getFacultyId(_inData.inLogin)
			if facultyId > -1:
				positionId = self.getPositionId(facultyId)
				if positionId > -1:
					position = self.getPosition(positionId)
					if position:
						pcn = position.get('PCN','')
						if 'E' not in pcn and 'W' not in pcn:
							print "%s,%s" % (pcn,_inData.eastywesty)


		# facultyId = self.getFacultyId(_inData.inLogin)
		# if facultyId > -1:
		# 	apptId = self.getAppointmentId(facultyId)
		# 	if apptId > -1:
		# 		self.updateApptDate(apptId,_inData.apptStart)

		# if not self.userExists(_inData.inLogin):
		# 	if not self.messageList: self.addProspect(_inData)
		# 	if not self.messageList: self.addPersonalInfo(_inData)
		# 	if not self.messageList: self.addFaculty(_inData)
		# 	if not self.messageList: self.assignPcn(_inData)
		# 	if not self.messageList: self.addPosition(_inData)
		# 	if not self.messageList: self.addPositionListItem(_inData)
		# 	if not self.messageList: self.addAppointment(_inData)
		# 	if not self.messageList: self.addJobAction(_inData)
		# 	if not self.messageList: self.addNewApptJobAction(_inData)
		# 	if not self.messageList: self.addUser(_inData)
		# 	if not self.messageList: self.addAuthority(_inData)
		#
		# 	if self.messageList:
		# 		self.nbrErrors += 1
		# 		self.logMessage("")
		# 		self.logMessage("Error processing %s: (%s %s)" % (_inData.getLogin(), _inData.getFname(), _inData.getLname()))
		# 		for message in self.messageList:
		# 			self.logMessage("  %s" % message)
		# 			print message
		# 			if message == "Unknown JobCode":
		# 				print _inData.getJobCode()
		# 			if message == "Unknown Department":
		# 				print _inData.getDept()

			#return

	def updateApptDate(self,apptId,apptStart):
		try:
			if apptStart.strip():
				dateParts = apptStart.split('/')
				dateParts[2] = '20' + dateParts[2]
				dateStr = "%s/%s/%s" % (dateParts[0],dateParts[1],dateParts[2])
				dt = datetime.datetime.strptime(dateStr, '%m/%d/%Y')
				dateVal = dt.date()
				sql = "update appointment set start_date = %s where id = %s"
				args = (dateVal,apptId)
				self.executeStatement(sql, args)
		except Exception,e:
			pass

	def getFacultyId(self,userId):
		sql = "select id from prospect where LOGIN_ID = %s"
		args = (userId,)
		qry = self.executeQuery(sql, _args=args)
		if len(qry) > 0:
			return qry[0]['id']
		return -1

	def getAppointmentId(self,facultyId):
		sql = "select id from appointment where faculty_id = %s"
		args = (facultyId,)
		qry = self.executeQuery(sql, _args=args)
		if len(qry) > 0:
			return qry[0]['id']
		return -1

	def getPositionId(self,facultyId):
		sql = "select position_id from appointment where faculty_id = %s"
		args = (facultyId,)
		qry = self.executeQuery(sql, _args=args)
		if len(qry) > 0:
			return qry[0]['position_id']
		return -1

	def getPosition(self,positionId):
		sql = "select * from position where id = %s"
		args = (positionId,)
		qry = self.executeQuery(sql, _args=args)
		if len(qry) > 0:
			return qry[0]
		return None


	def userExists(self,userid):
		sql = "select count(*) as count from users where username = '%s';" % (userid)
		qry = self.executeQuery(sql, _args=None)
		return qry[0]['count']

	def resolveDepartment(self, _inData):
		dept = _inData.getDept()
		if dept not in self.deptCache:
			self.messageList.append("Unknown Department '%s'" % dept)
			return
		_inData.setDepartmentId(self.deptCache[dept]['ID'])
		_inData.setPcnCode(self.deptCache[dept]['PCN_CODE'])

	def resolveJobCode(self, _inData):
		jobCode = _inData.getJobCode()
		if jobCode not in self.titleCache:
			self.messageList.append("Unknown JobCode '%s'" % jobCode)
			return

		_inData.setTitleId(self.titleCache[jobCode]['ID'])
		_inData.setTrackId(self.titleCache[jobCode]['TRACK_ID'])

	def resolveMetatrack(self, _inData):
		trackId = _inData.getTrackId()
		if not trackId:
			return

		if trackId not in self.trackCache:
			self.messageList.append("Unknown Track '%s'" % str(trackId))
			return
		_inData.setMetatrackId(self.trackCache[trackId]['METATRACK_ID'])

	def assignPcn(self, _inData):
		pcnDict = self.pcnCache.get(_inData.getPcnCode(), None)
		if not pcnDict:
			pcnDict = self.pcnCache[0L]

		pcn1 = pcnDict['ID']
		pcn2 = pcnDict['PCN'] + 1
		pcnDict['PCN'] = pcn2

		assignedPcn = "%02i-%05i" % (pcn1, pcn2)
		_inData.setAssignedPcn(assignedPcn)

	def addProspect(self, _inData):
		try:
			#LOGIN_ID,EMAIL,FIRST_NAME,LAST_NAME,APPT_REQ,NPI
			args = (_inData.getLogin(), _inData.getEmail(), _inData.getFname(), _inData.getLname(),_inData.getNPI())
			newId = self.executeInsertReturnId(PROSPECT_SQL, args)
			_inData.setProspectId(newId)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def getDate(self,str):
		returnVal = None
		try:
			if len(str) >= 8:
				parts = str.split('/')
				returnVal = datetime.date(int(parts[2]),int(parts[0]),int(parts[1]))
		except Exception,e:
			pass
		finally:
			return returnVal

	def getBool(self,str):
		returnVal = 0
		if str <> None:
			if str.upper() in ('Y','Yes','1','TRUE', 'ON'):
				returnVal = 1
		return returnVal


	def addPersonalInfo(self, _inData):
		try:
			args = (_inData.getProspectId(),
			        self.getDate(_inData.getDateOfBirth()),
			        _inData.getBirthCountry(),
			        _inData.getBirthState(),
			        _inData.getGender(),
			        self.getBool(_inData.getIsUSCitizen()),
			        self.getBool(_inData.getIsLivingInUS()),
			        self.getBool(_inData.getHasSSN()),
			        _inData.getEthnicity(),
			        _inData.getScholarlyFocus(),
			        _inData.getAliases(),
			        _inData.getLanguages(),
			        _inData.getAddress1(),
			        _inData.getAddress2(),
			        _inData.getAddress3(),
			        _inData.getAddress4(),
			        _inData.getCity(),
			        _inData.getState(),
			        _inData.getCountry(),
			        _inData.getZip(),
			        _inData.getPhone(),
			        _inData.getFax(),
			        _inData.getHdProgram(),
			        _inData.getHdDegree(),
			        _inData.getHdInstitution(),
			        _inData.getHdCountry(),
			        _inData.getHdState(),
			        _inData.getHdCity(),
			        _inData.getHdName(),
			        self.getDate(_inData.getHdStart()),
			        self.getDate(_inData.getHdEnd()),
			        self.getDate(_inData.getHdCompletedDate()),)
			newId = self.executeInsertReturnId(PERSONAL_INFO_SQL, args)
		except Exception, e:
			self.messageList.append(e.__repr__())


	def addFaculty(self, _inData):
		try:
			args = (_inData.getProspectId(),)
			self.executeStatement(FACULTY_SQL, args)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def addPosition(self, _inData):
		whichtype = ''
		dtypeUC = _inData.getType().upper()
		whichtype = 'PRIMARY'
		if dtypeUC.startswith('P'):
			whichtype = 'PRIMARY';
		elif dtypeUC.startswith('S'):
			whichtype = 'SECONDARY';

		try:
			args = (whichtype, _inData.getDepartmentId(), _inData.getMetatrackId(), _inData.getTitleId(), _inData.getAssignedPcn())
			newId = self.executeInsertReturnId(POSITION_SQL, args)
			_inData.setPositionId(newId)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def addPositionListItem(self, _inData):
		try:
			name = "%s, %s" % (_inData.getLname(), _inData.getFname())
			secondary = 0
			if _inData.getType().upper().startswith('S'): secondary = 1
			args = (_inData.getPositionId(), _inData.getAssignedPcn(), name, _inData.getDepartmentId(), _inData.getTitleId(), _inData.getProspectId(), secondary, self.actionDate)
			self.executeStatement(POSITION_LIST_ITEM_SQL, args)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def addAppointment(self, _inData):
		try:
			args = (_inData.getPositionId(), _inData.getTitleId(), _inData.getProspectId(), self.startDate)
			newId = self.executeInsertReturnId(APPOINTMENT_SQL, args)
			_inData.setAppointmentId(newId)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def addJobAction(self, _inData):
		try:
			args = (_inData.getAppointmentId(), _inData.getPositionId(), self.startDate)
			newId = self.executeInsertReturnId(JOB_ACTION_SQL, args)
			_inData.setJobActionId(newId)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def addNewApptJobAction(self, _inData):
		try:
			args = (_inData.getJobActionId(),)
			self.executeStatement(NEW_APPT_JOB_ACTION_SQL, args)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def addUser(self, _inData):
		try:
			args = (_inData.getLogin(),)
			self.executeStatement(USERS_SQL, args)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def addAuthority(self, _inData):
		try:
			args = (_inData.getLogin(),)
			self.executeStatement(AUTHORITIES_SQL, args)
		except Exception, e:
			self.messageList.append(e.__repr__())

	def savePcns(self):
		self.logMessage("Updating PCNs")
		for pcnDict in self.pcnCache.values():
			id = pcnDict['ID']
			pcn = pcnDict['PCN']
			try:
				args = (pcn, id)
				self.executeStatement(UPDATE_PCN_SQL, args)
			except Exception, e:
				self.messageList.append(e.__repr__())



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
		finally:
			if curs:
				curs.close()


	#	Logging

	def logSetup(self):
		if self.includeConsoleLog:
			print "%s Roster Load processor created" % (self.getLogTimestamp())
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

	class InData(object):
		def __init__(self, _splits,header):
			self.inLogin = _splits[header[kGLOBAL_ID]].strip()
			self.inEmail = _splits[header[kEMAIL_ADDRESS]].strip()
			self.inFname = _splits[header[kFIRST_NAME]].strip()
			self.inLname = _splits[header[kLAST_NAME]].strip()
			self.inDept = _splits[header[kDEPT_ID]].strip()
			self.inJobCode = _splits[header[kJOB_CODE]].strip()
			self.inType = _splits[header[kAPPOINTMENT_TYPE]].strip()

			self.middleInitial = _splits[header[kMIDDLE_INITIAL]].strip()
			self.suffix = _splits[header[kSUFFIX]].strip()
			self.npi = _splits[header[kNPI]].strip()
			self.dateOfBirth = _splits[header[kDATE_OF_BIRTH]].strip()
			self.gender = _splits[header[kGENDER]].strip()
			self.birthCountry = _splits[header[kBIRTH_COUNTRY]].strip()
			self.birthState = _splits[header[kBIRTH_STATE]].strip()
			self.isUSCitizen = _splits[header[kUS_CITIZEN]].strip()
			self.isLivingInUS = _splits[header[kLIVING_IN_US]].strip()
			self.hasSSN = _splits[header[kHAS_SSN]].strip()
			self.ethnicity = _splits[header[kETHNICITY]].strip()
			self.scholarlyFocus = _splits[header[kSCHOLARLY_FOCUS]].strip()
			self.aliases = _splits[header[kALIASES]].strip()
			self.languages = _splits[header[kLANGUAGES]].strip()
			self.address1 = _splits[header[kADDRESS_LINE1]].strip()
			self.address2 = _splits[header[kADDRESS_LINE2]].strip()
			self.address3 = _splits[header[kADDRESS_LINE3]].strip()
			self.address4 = _splits[header[kADDRESS_LINE4]].strip()
			self.city = _splits[header[kADDRESS_CITY]].strip()
			self.state = _splits[header[kADDRESS_STATE]].strip()
			self.country = _splits[header[kADDRESS_COUNTRY]].strip()
			self.zip = _splits[header[kADDRESS_ZIP]].strip()
			self.phone = _splits[header[kADDRESS_PHONE]].strip()
			self.fax = _splits[header[kADDRESS_FAX]].strip()
			self.hdProgram = _splits[header[kHD_PROGRAM]].strip()
			self.hdDegree = _splits[header[kHD_DEGREE]].strip()
			self.hdInstitution = _splits[header[kHD_INSTITUTION]].strip()
			self.hdCountry = _splits[header[kHD_COUNTRY]].strip()
			self.hdState = _splits[header[kHD_STATE]].strip()
			self.hdCity = _splits[header[kHD_CITY]].strip()
			self.hdName = _splits[header[kHD_NAME]].strip()
			self.hdStart = _splits[header[kHD_START]].strip()
			self.hdEnd = _splits[header[kHD_END]].strip()
			self.apptStart = _splits[header[kAPPT_START]].strip()
			self.eastywesty = _splits[header[kEASTYWESTY]].strip()

			#TODO - hdCompletedDate not defined in spreadsheet
			self.hdCompletedDate = ""

			self.prospectId = None
			self.departmentId = None
			self.pcnCode = None
			self.titleId = None
			self.trackId = None
			self.metatrackId = None
			self.positionId = None
			self.appointmentId = None
			self.jobActionId = None
			self.assignedPcn = None

		def getLogin(self): return self.inLogin
		def getEmail(self): return self.inEmail
		def getFname(self): return self.inFname
		def getLname(self): return self.inLname
		def getDept(self): return self.inDept
		def getJobCode(self): return self.inJobCode
		def getType(self): return self.inType

		#added
		def getMiddleInitial(self): return self.middleInitial
		def getSuffix(self): return self.suffix
		def getNPI(self): return self.npi if self.npi <> "" else None
		def getDateOfBirth(self): return self.dateOfBirth
		def getGender(self): return self.gender
		def getBirthCountry(self): return self.birthCountry
		def getBirthState(self): return self.birthState
		def getIsUSCitizen(self): return self.isUSCitizen
		def getIsLivingInUS(self): return self.isLivingInUS
		def getHasSSN(self): return self.hasSSN
		def getEthnicity(self): return self.ethnicity
		def getScholarlyFocus(self): return self.scholarlyFocus
		def getAliases(self): return self.aliases
		def getLanguages(self): return self.languages
		def getAddress1(self): return self.address1
		def getAddress2(self): return self.address2
		def getAddress3(self): return self.address3
		def getAddress4(self): return self.address4
		def getCity(self): return self.city
		def getState(self): return self.state
		def getCountry(self): return self.country
		def getZip(self): return self.zip
		def getPhone(self): return self.phone
		def getFax(self): return self.fax
		def getHdProgram(self): return self.hdProgram
		def getHdDegree(self): return self.hdDegree
		def getHdInstitution(self): return self.hdInstitution
		def getHdCountry(self): return self.hdCountry
		def getHdState(self): return self.hdState
		def getHdCity(self): return self.hdCity
		def getHdName(self): return self.hdName
		def getHdStart(self): return self.hdStart
		def getHdEnd(self): return self.hdEnd
		def getHdCompletedDate(self): return self.hdCompletedDate


		def getProspectId(self): return self.prospectId
		def setProspectId(self, _prospectId): self.prospectId = _prospectId

		def getDepartmentId(self): return self.departmentId
		def setDepartmentId(self, _departmentId): self.departmentId = _departmentId

		def getPcnCode(self): return self.pcnCode
		def setPcnCode(self, _pcnCode): self.pcnCode = _pcnCode

		def getTitleId(self): return self.titleId
		def setTitleId(self, _titleId): self.titleId = _titleId

		def getTrackId(self): return self.trackId
		def setTrackId(self, _trackId): self.trackId = _trackId

		def getMetatrackId(self): return self.metatrackId
		def setMetatrackId(self, _metatrackId): self.metatrackId = _metatrackId

		def getPositionId(self): return self.positionId
		def setPositionId(self, _positionId): self.positionId = _positionId

		def getAppointmentId(self): return self.appointmentId
		def setAppointmentId(self, _appointmentId): self.appointmentId = _appointmentId

		def getJobActionId(self): return self.jobActionId
		def setJobActionId(self, _jobActionId): self.jobActionId = _jobActionId

		def getAssignedPcn(self): return self.assignedPcn
		def setAssignedPcn(self, _assignedPcn): self.assignedPcn = _assignedPcn


class RosterInterface:
	DESCR = '''Roster is a cheesy little utility that reads a CSV file of people and generates data for import.'''

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
		return parser

	def run(self, options, args):
		try:
			roster = Roster(options, args)
			roster.process()
		except Exception, e:
			for each in e.args:
				print each
		finally:
			if roster:
				roster.shutdown()


if __name__ == '__main__':
	rosterInterface = RosterInterface()
	parser = rosterInterface.get_parser()
	(options, args) = parser.parse_args()
	rosterInterface.run(options, args)
