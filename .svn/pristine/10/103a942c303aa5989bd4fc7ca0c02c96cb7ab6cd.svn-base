# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
roster.py

Roster is a cheesy little script to load Faculty into the MARTA Roster.

Usage:

$ python /path/to/roster.py -i /path/to/tab/delimited/file.csv

'''

import codecs
import datetime
import optparse
import os
import os.path
import sys
import MySQLdb as mysqldb

DEPARTMENT_SQL = '''SELECT * FROM DEPARTMENT'''
TITLE_SQL = '''SELECT * FROM TITLE WHERE ACTIVE = 1'''
TRACK_SQL = '''SELECT * FROM TRACK'''
PCN_SQL = '''SELECT * FROM PCN_CODE'''
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

class Roster(object):

	#	Initialization

	def __init__(self, options=None, args=None):
		self.srcPath = "source not specified"
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
		
		self.startDate = datetime.date(2012,4,1)
		self.actionDate = datetime.datetime(2012,4,1)
		self.today = datetime.date.today()
		self.includeConsoleLog = True

		self.nbrIgnored = 0
		self.nbrProcessed = 0
		self.nbrErrors = 0
		
		if options:
			if options.srcPath: self.srcPath = os.path.abspath(options.srcPath)
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
		
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
			for line in srcFile:
				trimmedLine = line.strip()
				if trimmedLine.startswith("LOGIN_ID"):
					self.nbrIgnored += 1
					continue
				splits = trimmedLine.split("\t")
				if len(splits) < 7:
					self.nbrIgnored += 1
				else:
					self.processOneLine(Roster.InData(splits))
			
		finally:
			if srcFile is not None:
				try: srcFile.close()
				except Exception, e: pass

	def processOneLine(self, _inData):
		self.nbrProcessed += 1
		self.messageList = []
		self.resolveDepartment(_inData)
		self.resolveJobCode(_inData)
		self.resolveMetatrack(_inData)
		
		if not self.messageList: self.addProspect(_inData)
		if not self.messageList: self.addFaculty(_inData)
		if not self.messageList: self.assignPcn(_inData)
		if not self.messageList: self.addPosition(_inData)
		if not self.messageList: self.addPositionListItem(_inData)
		if not self.messageList: self.addAppointment(_inData)
		if not self.messageList: self.addJobAction(_inData)
		if not self.messageList: self.addNewApptJobAction(_inData)
		if not self.messageList: self.addUser(_inData)
		if not self.messageList: self.addAuthority(_inData)
		
		if self.messageList:
			self.nbrErrors += 1
			self.logMessage("")
			self.logMessage("Error processing %s: (%s %s)" % (_inData.getLogin(), _inData.getFname(), _inData.getLname()))
			for message in self.messageList:
				self.logMessage("  %s" % message)
			return

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
			args = (_inData.getLogin(), _inData.getEmail(), _inData.getFname(), _inData.getLname())
			newId = self.executeInsertReturnId(PROSPECT_SQL, args)
			_inData.setProspectId(newId)
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
		def __init__(self, _splits):
			self.inLogin = _splits[0].strip()
			self.inEmail = _splits[1].strip()
			self.inFname = _splits[2].strip()
			self.inLname = _splits[3].strip()
			self.inDept = _splits[4].strip()
			self.inJobCode = _splits[5].strip()
			self.inType = _splits[6].strip()
			
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
		parser.add_option('-i', '--src', dest='srcPath', default='', help='path to source file')
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
