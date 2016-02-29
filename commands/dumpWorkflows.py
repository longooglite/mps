# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
dumpworkflows.py

works on MacOS - dumps workflow files to desktop
'''
import json
import sys
import os
import pprint
import os.path
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import logging
import logging.config
import optparse
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.core.constants
import cStringIO


class WFDump(object):
	def __init__(self, options=None, args=None, _db=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'mpsdev'
		self.user = 'mps'
		self.password = 'mps'
		self.db = _db

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password

	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		try:
			if not self.db:
				self.connectToDatabase()
			self.createDesktopDirs()
			workFlows = self.getWorkFlows()
			for workFlow in workFlows:
				if len(workFlow['src']) > 0:
					filename = workFlow['code'] + ".py"
					if workFlow['is_site_override']:
						path = self.buildPathHierarchy(os.path.expanduser("~/Desktop/") + "workflows%ssites%s" % (os.sep,os.sep),workFlow.get('car_relative_path','')) + filename
					else:
						path = os.path.expanduser("~/Desktop/") + "workflows%score%s" % (os.sep,os.sep) + filename
					f = open(path,'w')
					f.write(workFlow['src'])
					f.close()
			titleOverrides = self.getTitleOverrides()
			filename = "overrides.py"
			overrideList = []
			for each in titleOverrides:
				overrideList.append(json.loads(each['value']))
			path = os.path.expanduser("~/Desktop/") + "workflows%ssite%soverrides%s" % (os.sep,os.sep,os.sep) + filename
			f = open(path,'w')
			f.write("overrides = " + json.dumps(overrideList,indent=4))

			f.close()

		except Exception, e:
			print e.message

	def buildPathHierarchy(self,writePath,car_relativePath):
		pathParts = car_relativePath.split(os.sep)
		currentPath = writePath
		for each in pathParts:
			if each and each <> 'sites' and not each.endswith('.py'):
				currentPath += each + os.sep
				if not os.path.exists(currentPath):
					os.makedirs(currentPath)
		return currentPath

	def createDesktopDirs(self):
		try:
			os.makedirs(os.path.expanduser("~/Desktop/") + "workflows%score%s" % (os.sep,os.sep))
			os.makedirs(os.path.expanduser("~/Desktop/") + "workflows%ssites%s" % (os.sep,os.sep))
			os.makedirs(os.path.expanduser("~/Desktop/") + "workflows%ssite%soverrides%s" % (os.sep,os.sep,os.sep))
		except:
			pass

	def getTitleOverrides(self):
		return self.db.executeSQLQuery("SELECT * FROM wf_component_override",())

	def getWorkFlows(self):
		return self.db.executeSQLQuery("SELECT * FROM wf_component",())

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)


class WFDumpInterface:
	DESCR = '''atram workflow dump'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsdev', help='database name (default=mpsdev')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')

		return parser

	def run(self, options, args):
		wfLoad = None
		try:
			wfDump = WFDump(options, args)
			wfDump.process()
		except Exception, e:
			print e.message
		finally:
			if wfLoad:
				wfLoad.shutdown()


if __name__ == '__main__':
	logging.config.fileConfig(cStringIO.StringIO(MPSCore.core.constants.kDebugFormatFile))
	import MPSCore.utilities.sqlUtilities as sqlUtilities

	dataLoadInterface = WFDumpInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
