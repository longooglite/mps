# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
atramRosterLoad.py

#REQUIRED - need to load workflows prior to running roster load to ensure there is a new appointment job action in place.
'''

import sys
import os
import os.path
import csv
import uuid
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import logging
import logging.config
import optparse
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.core.constants
import datetime
import cStringIO
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.services.lookupTableService as lookupTableService



class AtramRosterLoad(object):

	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'umms'
		self.user = 'mps'
		self.password = 'mps'
		self.db = None
		self.messageList = []
		self.site = 'umms'
		self.destroy = '0'
		self.delimitter = '|'

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.site: self.site = options.site
			if options.destroy: self.destroy = options.destroy
			if options.delimitter: self.delimitter = options.delimitter

	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		counter = 0
		try:
			self.connectToDatabase()
			jaType = lookupTableService.getEntityByKey(self.db,'wf_job_action_type',"NEWAPPOINT","code")
			self.job__action_type_id = jaType.get('id')
			fileData = self.getImportFileBySite("ummsroster.txt")
			if self.destroy == '1':
				self.doDestroy()
			for row in fileData:
				try:
					counter += 1
					if not row[0].startswith('#') and not row == []:
						rowDict = self.getRowDict(row)
						rowDict = self.resolveKeys(rowDict)
						rowDict['person_id'] = self.importPerson(rowDict)
						rowDict['position_id'] = self.importPosition(rowDict)
						rowDict['appointment_id'] = self.importAppointment(rowDict)
						self.db.executeSQLCommand("commit;")

						#self.importJobAction(rowDict)
				except Exception,e:
					self.db.executeSQLCommand("rollback;")
					pass
			self.resetPCNSequences()
			print counter
		except Exception, e:
			print e.message
			pass

	def doDestroy(self):
		self.db.executeSQLCommand("delete from wf_job_action")
		self.db.executeSQLCommand("delete from wf_appointment")
		self.db.executeSQLCommand("delete from wf_position")
		self.db.executeSQLCommand("delete from wf_person")

	def resetPCNSequences(self):
		sql = "select code from wf_pcn"
		pcns = self.db.executeSQLQuery(sql,())
		for each in pcns:
			term = each['code'] + '-'
			sql = "SELECT MAX(pcn) FROM wf_position WHERE pcn LIKE %(like)s;"
			qry = self.db.executeSQLQuery(sql,dict(like=term+'%'))
			if qry[0]['max']:
				splits = qry[0]['max'].split('-')
				code = splits[0]
				nextId = int(splits[1]) +1
				sql = "UPDATE wf_pcn SET seq = %s WHERE code = %s"
				args = (nextId,code,)
				self.db.executeSQLCommand(sql,args)

	def importPerson(self,rowDict):
		sql = '''INSERT INTO wf_person (community,username,first_name,last_name,suffix,middle_name,email,employee_nbr,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
		args = (rowDict.get('community','default'),
				rowDict.get('username','').lower(),
				rowDict.get('first_name',''),
				rowDict.get('last_name',''),
				rowDict.get('suffix',''),
				rowDict.get('middle_name',''),
				rowDict.get('email',''),
				rowDict.get('employee_nbr',''),
				rowDict.get('now',''),
				rowDict.get('now',''),
				rowDict.get('lastuser',''),)
		qry = self.db.executeSQLQuery(sql,args)
		if qry:
			return qry[0]['id']

	def importPosition(self,rowDict):
		pcn = rowDict.get('pcn','')
		if not pcn:
			pcn = self.getPCN(rowDict.get('department_id',None))

		sql = '''INSERT INTO wf_position (department_id,title_id,pcn,is_primary,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
		args = (rowDict.get('department_id',None),
				rowDict.get('title_id',None),
				pcn,
				rowDict.get('is_primary',True),
				rowDict.get('now',''),
				rowDict.get('now',''),
				rowDict.get('lastuser',''),)
		qry = self.db.executeSQLQuery(sql,args)
		if qry:
			return qry[0]['id']

	def getPCN(self,department_id):
		pcnNumber = ''
		sql = "SELECT pcn_id FROM wf_department WHERE id = %s"
		args = (department_id,)
		deptQry = self.db.executeSQLQuery(sql,args)
		if deptQry:
			pcn_id = deptQry[0]['pcn_id']
			sql = "SELECT * FROM wf_pcn WHERE id = %s"
			args = (pcn_id,)
			pcnQry = self.db.executeSQLQuery(sql,args)
			if pcnQry:
				pcnNumber = self.formatPcn(pcnQry[0])
				seq = pcnQry[0]['seq'] + 1
				sql = "UPDATE wf_pcn SET seq = %s WHERE id = %s"
				args = (seq,pcnQry[0]['id'])
				self.db.executeSQLCommand(sql,args)

		return pcnNumber

	def formatPcn(self,_pcnDict, _pcnFormatString='%s-%05d'):
		return _pcnFormatString % (_pcnDict.get('code',None), _pcnDict.get('seq',None))


	def importAppointment(self,rowDict):
		sql = '''INSERT INTO wf_appointment (person_id,title_id,position_id,start_date,end_date,appointment_status_id,created,updated,lastuser) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id'''
		args = (rowDict.get('person_id',None),
				rowDict.get('title_id',None),
				rowDict.get('position_id',None),
				rowDict.get('start_date',''),
				rowDict.get('end_date',''),
				rowDict.get('appointment_status_id',None),
				rowDict.get('now',''),
				rowDict.get('now',''),
				rowDict.get('lastuser',''))
		qry = self.db.executeSQLQuery(sql,args)
		if qry:
			return qry[0]['id']

	def resolveKeys(self,rowDict):
		rowDict['title_id'] = self.getTableKey('wf_title',rowDict.get('titlecode'), lookupfield = 'job_code')
		rowDict['department_id'] = self.getTableKey('wf_department',rowDict.get('deptcode'))
		rowDict['appointment_status_id'] = self.getFilledAppointmentStatusId()
		rowDict['workflow_id'] = self.getNewAppointmentWorkflowId()
		rowDict['now'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
		rowDict['lastuser'] = "initial import"
		return rowDict

	def getRowDict(self,row):
		rowDict = {}
		rowDict['community'] = 'default'
		rowDict['username'] = row[0].strip()
		rowDict['first_name'] = row[1].strip()
		rowDict['last_name'] = row[2].strip()
		rowDict['middle_name'] = row[3].strip()
		rowDict['suffix'] = row[4].strip()
		rowDict['email'] = row[5].strip()
		rowDict['employee_nbr'] = row[6].strip()
		rowDict['deptcode'] = row[7].strip()
		rowDict['pcn'] = row[8].strip()
		rowDict['is_primary'] = self.resolveBoolean(row[9].strip())
		rowDict['titlecode'] = row[10].strip()
		rowDict['start_date'] = self.resolveDate(row[11].strip())
		rowDict['end_date'] = self.resolveDate(row[12].strip())
		return rowDict

	def resolveDate(self,value):
		if value:
			splits = value.split("/")
			try:
				y = int(splits[2])
				m = int(splits[0])
				d = int(splits[1])
				adate = datetime.date(y,m,d)
				returnValue = dateUtils.formatUTCDateOnly(adate)
				return returnValue
			except Exception, e:
				print "invalid start/end date format."
				return ''
		else:
			return ''

	def resolveBoolean(self,value):
		if value.upper() in ('1','ON','T','TRUE','YES','Y'):
			return True
		return False

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)

	def getTableKey(self,tableName,code,lookupfield = 'code'):
		sql = "select id from %s where %s = '%s'" % (tableName,lookupfield,code)
		qry = self.db.executeSQLQuery(sql,())
		if len(qry) > 0:
			return qry[0]['id']

	def getFilledAppointmentStatusId(self):
		sql = "select id from wf_appointment_status where code = 'FILLED'"
		qry = self.db.executeSQLQuery(sql,())
		if len(qry) > 0:
			return qry[0]['id']

	def getNewAppointmentWorkflowId(self):
		sql = "SELECT id from wf_workflow WHERE job_action_type_id = (SELECT id FROM wf_job_action_type WHERE code = 'NEWAPPOINT');"
		qry = self.db.executeSQLQuery(sql,())
		if len(qry) > 0:
			return qry[0]['id']

	def getImportFileBySite(self, fileName):
		filepath = os.path.abspath(__file__).split("car")[0] + "car%sdata%satramData%ssites%s%s%s" % (os.sep,os.sep,os.sep,os.sep,self.site,os.sep) + fileName
		f = open(filepath, 'rU')
		data = list(csv.reader(f, delimiter=self.delimitter))
		f.close()
		return data

	def getImportFile(self, fileName):
		filepath = os.path.abspath(__file__).split("car")[0] + "car%sdata%satramData%s" % (os.sep,os.sep,os.sep) + fileName
		f = open(filepath, 'rU')
		data = list(csv.reader(f, delimiter=self.delimitter))
		f.close()
		return data



class DataLoadInterface:
	DESCR = '''Data Load for Atram. Currently loads only lookup data.'''

	def __init__(self):
		pass

	def get_parser(self):

		#REQUIRED - need to load workflows prior to running roster load to ensure there is a new appointment job action in place for historical job actions

		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=5432)')
		parser.add_option('-d', '--dbname', dest='dbname', default='umms', help='database name (default=mpsdev')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-s', '--site', dest='site', default='umms', help='data for this site is loaded from /data/atramData/sites/{sitename}')
		parser.add_option('-x', '--destroy', dest='destroy', default="0", help='destroy existing data. 1=on, 0=off')
		parser.add_option('-l', '--delimitter', dest='delimitter', default="|", help='delimitter')

		return parser

	def run(self, options, args):
		atramLoad = None
		try:
			atramLoad = AtramRosterLoad(options, args)
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
