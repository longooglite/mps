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
import random
import optparse
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import MPSCore.utilities.dbConnectionParms as dbConnParms
import uuid


class RoosterLoad(object):

	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'mpsdev'
		self.user = 'mps'
		self.password = 'mps'
		self.db = None
		self.messageList = []
		self.lastPersonId = 0


		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.rostersize: self.rosterSize = int(options.rostersize)
			if options.appointmentsize: self.appointSize = int(options.appointmentsize)
			if options.emptyposize: self.emptyPositionSize = int(options.emptyposize)
			if options.secondarysize: self.secondarySize = int(options.secondarysize)

	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		try:
			self.connectToDatabase()
			self.lastPersonId = self.getLastPerson()
			self.roosterLoad()
		except Exception, e:
			print e.message

	def getLastPerson(self):
		sql = "select max(id) as id from wf_person"
		qry = self.db.executeSQLQuery(sql,())
		return qry[0]['id'] if qry else 0

	def roosterLoad(self):
		self.loadPerms()
		self.loadPeople()
		self.loadPositions(True,self.rosterSize)
		self.loadAppointments()
		self.loadJobActions()
		#empty positions
		self.loadPositions(True,self.emptyPositionSize)
		#secondary positions
		self.loadPositions(False,self.secondarySize)
		self.loadSecondaryAppointments()

	def loadPerms(self):
		alldepts = self.db.executeSQLQuery("select id from wf_department")
		sql = "INSERT INTO wf_username_department (username,department_id) VALUES ('eric',%s);"
		for each in alldepts:
			try:
				self.db.executeSQLCommand(sql,(each['id'],))
				self.db.executeSQLCommand("commit")
			except:
				self.db.executeSQLCommand("rollback")
				pass

	def loadSecondaryAppointments(self):
		people = self.getPeople()
		secondaries = self.db.executeSQLQuery("select * from wf_position where is_primary = 'f'",())
		for each in secondaries:
			statusId = random.randint(1,2)
			person = people[random.randint(1,self.rosterSize)]
			self.insertAppointment(person['id'],each['title_id'],each['id'],statusId)


	def loadJobActions(self):
		appts = self.getAppointments()
		for appt in appts:
			sql = '''INSERT INTO wf_job_action (person_id,position_id,appointment_id,current_status,workflow_id,workflow_json,complete,frozen,revisions_required,created,updated,completed,lastuser) VALUES (%s,%s,%s,'',1,'','f','f','f','2010-10-10','2010-10-10','','eric');'''
			args = (appt['person_id'],appt['position_id'],appt['id'],)
			self.db.executeSQLCommand(sql,args)

	def getAppointments(self):
		sql = "select * from wf_appointment limit %i" % (self.appointSize)
		return self.db.executeSQLQuery(sql,())

	def loadAppointments(self):
		people = self.getPeople()
		titlesAndPositions = self.getTitlesAndPositions()
		i = 0
		for peep in people:
			statusId = random.randint(1,2)
			self.insertAppointment(peep['id'],titlesAndPositions[i]['title_id'],titlesAndPositions[i]['id'],statusId)
			i += 1

	def insertAppointment(self,person_id,title_id,position_id,status_id):
		sql = '''INSERT INTO wf_appointment (person_id,title_id,position_id,start_date,end_date,appointment_status_id,created,updated,lastuser) VALUES (%s,%s,%s,'2010-10-10','2010-10-10',%s,'2010-10-10','2010-10-10','eric');'''
		args = (person_id,title_id,position_id,status_id,)
		self.db.executeSQLCommand(sql,args)


	def loadPositions(self,isPrimary = True,size = 0):
		for i in range(0,size):
			departmentId = random.randint(1,50)
			titleId = random.randint(1,50)
			pcn = self.getPCN(departmentId)
			sql = '''INSERT INTO wf_position (department_id,title_id,pcn,is_primary,created,updated,lastuser) VALUES (%s,%s,%s,%s,'2010-10-10','2010-10-10','eric');'''
			args = (departmentId,titleId,pcn,isPrimary)
			self.db.executeSQLCommand(sql,args)

	def getPCN(self,deptId):
		pcnIdQry = self.db.executeSQLQuery("select wf_pcn.id,wf_pcn.code,wf_pcn.seq from wf_department,wf_pcn where wf_department.id = %s and pcn_id = wf_pcn.id", (deptId,))
		newSeq = pcnIdQry[0]['seq'] + 1
		self.db.executeSQLCommand("update wf_pcn set seq = %s where id = %s", (newSeq,pcnIdQry[0]['id'],))
		return pcnIdQry[0]['code'] + '-' + str(newSeq)

	def loadPeople(self):
		for i in range(0,self.rosterSize):
			sql = '''INSERT INTO wf_person (username,first_name,last_name,suffix,middle_name,email,employee_nbr,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,'','2010-01-01 12:12:12','2010-01-01 12:12:12','eric');'''
			args = (self.someRandomValue().lower(),self.someRandomValue(),self.someRandomValue(),self.someRandomValue(),self.someRandomValue(),self.someRandomValue(),)
			self.db.executeSQLCommand(sql,args)

	def getTitlesAndPositions(self):
		sql = "select id,title_id from wf_position"
		return self.db.executeSQLQuery(sql,())

	def getPeople(self):
		sql = "select id from wf_person where id > %s"
		return self.db.executeSQLQuery(sql,(self.lastPersonId,))

	def someRandomValue(self):
		firstLetter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
		return firstLetter + ''.join(random.choice(['ar','el','ba','ab','an','roo','chao','au','ast','ass','quo','tar','rah','moo','au','mor','le','la','lee','ith','boo','choo']) for i in range(random.randint(2,4)))


	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)


class DataLoadInterface:
	DESCR = '''Overload a roster with meaningless shit'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsdev', help='database name (default=mpsdev')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-r', '--rsize', dest='rostersize', default=3000, help='roster size')
		parser.add_option('-a', '--asize', dest='appointmentsize', default=3000, help='appointment size')
		parser.add_option('-e', '--esize', dest='emptyposize', default=200, help='empty positions')
		parser.add_option('-s', '--ssize', dest='secondarysize', default=200, help='secondary positions')

		return parser

	def run(self, options, args):
		try:
			roosterLoad = RoosterLoad(options, args)
			roosterLoad.process()
		except Exception, e:
			print e.message
		finally:
			if roosterLoad:
				roosterLoad.shutdown()


if __name__ == '__main__':
	import MPSCore.utilities.sqlUtilities as sqlUtilities

	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
