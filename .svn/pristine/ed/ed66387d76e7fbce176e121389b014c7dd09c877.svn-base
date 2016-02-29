# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''

'''
import optparse
import os
import os.path
import sys
import json
import subprocess
import commands

sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.sqlUtilities as sqlUtilities

'''Place system into "maintenance mode", where user will see a page telling them the site is under maintenance,
vs a login dialog. This can be done for all sites, by default, or by site.
When putting all sites into maintenance mode, all processes will be killed except for MPSLogin.py.
When putting a single site into maintenance mode, no processes will be killed.
Likewise, when turning maintenance mode off, processes, by default, will be restarted.
To kill, or not to kill, that is the question. For the meek of heart, killing can be killed via
a command line parameter.'''

path = "%stmp%smaintenancemode.json" % (os.sep,os.sep)

class MaintenanceMode(object):

	#	Initialization

	def __init__(self, options=None, args=None):
		self.mode = options.mode
		self.site = options.site
		self.killprocesses = options.killprocesses
		self.host = options.host
		self.port = int(options.port)
		self.dbname = options.dbname
		self.user = options.user
		self.password = options.password
		self.additionalMessage = options.additionalMessage
		self.environment = options.environment
		self.db = None
		self.connectToDatabase()

	#	Shutdown

	def shutdown(self):
		self.db.closeMpsConnection()

	#	Execution

	def process(self):
		try:
			if self.mode == 'on':
				if not self.alreadyInMaintenanceMode():
					self.updateMaintenanceModePreference()
					if self.site == 'all' and self.killprocesses == 'y':
						self.killMPSProcesses()
				else:
					print "System is already in maintenance mode. Nothing was done."
					sys.exit(0)
			else:
				if self.alreadyInMaintenanceMode():
					self.updateMaintenanceModePreference()
					if self.site == 'all' and self.killprocesses == 'y':
						self.startMPSProcesses()
				else:
					print "System is not in maintenance mode. Nothing was done."
					sys.exit(0)
		except Exception,e:
			for each in e:
				print e.args

	def alreadyInMaintenanceMode(self):
		return True if os.path.exists(path) else False

	def updateMaintenanceModePreference(self):
		if self.mode == 'off':
			if os.path.exists(path):
				os.remove(path)
		if self.mode == 'on':
			siteDict = {}
			siteDict['additionalMessage'] = self.additionalMessage
			if self.site == 'all':
				sql = "SELECT code FROM site"
				sites = self.db.executeSQLQuery(sql,args)
				for each in sites:
					siteDict[each['code']] = "true"
			else:
				siteDict[self.site] = "true"
			f = open(path,'w')
			f.write(json.dumps(siteDict))
			f.flush()
			f.close()

	def killMPSProcesses(self):
		processDict = {"MPSAuthSvc.py":False,
		               "MPSAdmin.py":False,
		               "MPSCV.py":False,
		               "MPSAppt.py":False,
		               }
		processoutput = subprocess.Popen(['ps', '-eo' 'pid,command'], stdout=subprocess.PIPE).communicate()[0].split("\n")
		for process in processoutput:
			for processName in processDict:
				processId = ''
				foundProcess = False
				if process.find(processName) > 0:
					foundProcess = True
					processId = self.getProcessId(process)
				if processId <> '':
					result = commands.getoutput("kill -9 %s" % (processId))
					print "killing %s-%s" % (processId,processName)
					if result <> '':
						print "%s - returned when trying to kill %s" % (result,processName)
					else:
						print "%s is dead" % (processName)
					processDict[processName] = True
				else:
					if foundProcess:
						print "Unable to parse process id for %s. This process was not killed." % (processName)
		for processName in processDict:
			if not processDict[processName]:
				print "The process for %s was not found and was not killed" % (processName)


	def getProcessId(self,process):
		slice = process.strip()[0:process.strip().find(' ')+1].strip()
		if self.isint(slice):
			return slice
		return ''

	def isint(self,x):
		try:
			a = float(x)
			b = int(a)
		except ValueError:
			return False
		else:
			return a == b

	def startMPSProcesses(self):
		root = os.path.abspath(__file__).split("car")[0] + "car" + os.sep
		print "running skynard"
		command = "%s %s" % ("python",root + "commands/skynyrd.py")
		result = commands.getoutput(command)

		print "starting MPSAuthSvc"
		command = "%s %s" % ("python",root + "MPSAuthSvc.py -e %s &" % (self.environment))
		os.system(command)

		print "starting MPSAdmin"
		command = "%s %s" % ("python",root + "MPSAdmin.py -e %s &" % (self.environment))
		os.system(command)

		print "starting MPSCV"
		command = "%s %s" % ("python",root + "MPSCV.py -e %s &" % (self.environment))
		os.system(command)

		command = "%s %s" % ("python",root + "MPSCV.py -e %s --file config/%s/MPSCV/config1.json &" % (self.environment,self.environment))
		os.system(command)

		print "starting MPSAppt"
		command = "%s %s" % ("python",root + "MPSAppt.py -e %s &" % (self.environment))
		os.system(command)

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)

class Maintainface:
	def __init__(self):
		print "Running..."

	def get_parser(self):
		descr = '''Place system into "maintenance mode. This can be done for all sites, by default, or by site. When putting all sites in maintenance mode, all processes will be killed except for MPSLogin.py. When putting a single site into maintenance mode, no processes will be killed. Likewise, when turning maintenance mode off, processes that were killed will be restarted. "'''
		parser = optparse.OptionParser(description=descr)
		parser.add_option('-m', '--mode', dest='mode', default='off', help='place system into or out of maintenance mode. on/off')
		parser.add_option('-a', '--additionalMessage', dest='additionalMessage', default='', help='additional message to display on maintenance screen. Use quoted string as argument.')
		parser.add_option('-s', '--site', dest='site', default='all', help='place single or all site(s) into maintenance mode. Default is all sites')
		parser.add_option('-k', '--killp', dest='killprocesses', default='y', help='kill processes. Does not work for a single site')
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsauth', help='database name (default=mpsauth')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-e', '--environment', dest='environment', default='devserver', help='environment e.g. devserver, prod1server, etc. Default = devserver')

		return parser

	def run(self, options, args):
		maintenanceMode = None
		try:
			maintenanceMode = MaintenanceMode(options, args)
			maintenanceMode.process()
			print "Maintenance mode was set to: %s" % (options.mode)
		except Exception, e:
			for each in e.args:
				print each
		finally:
			if maintenanceMode:
				maintenanceMode.shutdown()


if __name__ == '__main__':
	maintainface = Maintainface()
	parser = maintainface.get_parser()
	(options, args) = parser.parse_args()
	maintainface.run(options, args)
