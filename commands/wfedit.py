# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import sys
import os
import os.path
import optparse
import pprint
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSAppt.services.workflowEditService as WFEditor
import dumpWorkflows


'''
--view all container codes, descriptions and types
python wfedit.py --viewcodes 1

--view a container
python wfedit.py --viewcontainer item1

--add new workflow
python wfedit.py --createwf testwf1 test PROMOTION

--add tab to workflow
python wfedit.py --addtab testwf1 tab1 tab1

--add section to tab
python wfedit.py --addsection testwf1 tab1 sect1 sect1

--add item to section
python wfedit.py --additem testwf1 tab1 sect1 item1 item1 FileUpload

--add container to any other container
python wfedit.py --addcontainer parentcode childcode childdescr

--rename component
python wfedit.pt --renamecontainer existingcode newcode newdescr

--update key/value pair -note this is not the end all component editor. It does not take into account data types such as lists, booleans, etc.
it does support simple nesting, such as adding a value to the config dictionary

add value to the config dict
python wfedit.pt --updatekv taskA config.someattr value

add value to the component dict
python wfedit.pt --updatekv taskA someattr value

--dump all workflows to desktop
python wfedit.py --dump 1


'''


createWfArgs = ['workflowcode', 'workflowdescr', 'jobactiontypecode']
addTabArgs = ['workflowcode', 'tabcode', 'tabdescr', 'optionalposition']
addSectionArgs = ['workflowcode', 'tabcode', 'sectioncode', 'sectiondescr', 'optionalposition']
addItemArgs = ['workflowcode', 'tabcode', 'sectioncode', 'itemcode', 'itemdescr', 'classname', 'optionalposition']
renameContainerArgs = ['containercode', 'newcode', 'optionalnewdescr']
addContainerArgs = ['parentcontainercode', 'code', 'descr']
dumpWorkFlowArgs = ['workflowcode']
viewContainerArgs = ['workflowcode']
updateKVArgs = ['containercode', 'key', 'value']

class Command:
	def __init__(self,_dbConnection,_options,_args):
		self.options = _options
		self.args = _args
		self.wfEditSvc = WFEditor.WorkflowService(_dbConnection)
		self.dbConnection = _dbConnection

	def run(self):
		if self.options.createwf:
			if self.validateArgs(createWfArgs):
				self.createWorkflow()
		elif self.options.addtab:
			if self.validateArgs(addTabArgs):
				self.addTab()
		elif self.options.addsection:
			if self.validateArgs(addSectionArgs):
				self.addSection()
		elif self.options.additem:
			if self.validateArgs(addItemArgs):
				self.addItem()
		elif self.options.renamecontainer:
			if self.validateArgs(renameContainerArgs):
				self.renameContainer()
		elif self.options.addcontainer:
			if self.validateArgs(addContainerArgs):
				self.addContainer()
		elif self.options.dump:
			self.dumpWorkflows()
		elif self.options.viewcontainer:
			self.viewContainer(options.viewcontainer)
		elif self.options.updatekv:
			if self.validateArgs(updateKVArgs):
				self.updateKV()
		elif self.options.viewcodes:
			self.viewContainerCodes()
		else:
			print "Nothing to do"

	def validateArgs(self,requirements):
		passed = self.countPassedArguments()
		required = self.countRequirements(requirements)
		if passed < required:
			print "Invalid number of arguments. Arguments are:"
			for arg in requirements:
				print arg
		return passed >= required

	def countPassedArguments(self):
		nubber = 1
		for arg in self.args:
			nubber += 1
		return nubber

	def countRequirements(self,requirements):
		nubber = 0
		for requirement in requirements:
			if not requirement.startswith('opt'):
				nubber += 1
		return nubber

	def createWorkflow(self):
		print "createworkflow"
		argsDict = self.getArgsDict(createWfArgs,self.options.createwf)
		result = self.wfEditSvc.createWorkflow(argsDict)
		print result

	def addTab(self):
		print "addTab"
		argsDict = self.getArgsDict(addTabArgs,self.options.addtab)
		result = self.wfEditSvc.addTab(argsDict)
		print result

	def addSection(self):
		print "addSection"
		argsDict = self.getArgsDict(addSectionArgs,self.options.addsection)
		result = self.wfEditSvc.addSection(argsDict)
		print result

	def addItem(self):
		print "addItem"
		argsDict = self.getArgsDict(addItemArgs,self.options.additem)
		result = self.wfEditSvc.addItem(argsDict)
		print result

	def renameContainer(self):
		print "renameContainer"
		argsDict = self.getArgsDict(renameContainerArgs,self.options.renamecontainer)
		result = self.wfEditSvc.renameContainer(argsDict)
		print result

	def addContainer(self):
		print "addContainer"
		argsDict = self.getArgsDict(addContainerArgs,self.options.addcontainer)
		result = self.wfEditSvc.addContainer(argsDict)
		print result

	def dumpWorkflows(self):
		print "dumpWorkflows"
		dumper = dumpWorkflows.WFDump(None,None,self.dbConnection)
		dumper.process()

	def viewContainer(self,workflowCode):
		print "viewContainer"
		containerDict = self.wfEditSvc.getContainerDict(workflowCode)
		if containerDict:
			print pprint.pformat(containerDict,4)
		else:
			print "Unable to find container"

	def viewContainerCodes(self):
		print "viewcontainercodes"
		codes = self.wfEditSvc.getAllCodes()
		longestCode = self.getLongestEntry(codes)
		for code in codes:
			print ("%s\t%s - %s") % (code.get('code','').rjust(longestCode),code.get('descr',''),code.get('wftype',''))

	def getLongestEntry(self,codes,key='code'):
		longest = 0
		for code in codes:
			l = len(code.get('code',''))
			longest = l if l > longest else longest
		return longest

	def updateKV(self):
		print "updatekv"
		argsDict = self.getArgsDict(updateKVArgs,self.options.updatekv)
		result = self.wfEditSvc.updateKV(argsDict)
		print result

	def getArgsDict(self,requirements,option):
		svcParams = {}
		svcParams[requirements[0]] = option
		counter = 0
		for req in requirements:
			if counter > 0:
				svcParams[req] = ''
				if len(self.args) >= counter:
					svcParams[req] = self.args[counter-1]
			counter += 1
		return svcParams

class CommandLineInterface:
	DESCR = ''''''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsdev', help='database name (default=mpsdev')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')

		parser.add_option('-1', '--createwf', dest='createwf', default='', help='create workflow - args = %s' % (','.join(createWfArgs)))
		parser.add_option('-2', '--addtab', dest='addtab', default='', help='add tab to workflow - args = %s' % (','.join(addTabArgs)))
		parser.add_option('-3', '--addsection', dest='addsection', default='', help='add section to workflow - args = %s' % (','.join(addSectionArgs)))
		parser.add_option('-4', '--additem', dest='additem', default='', help='add item to workflow - args = %s' % (','.join(addItemArgs)))
		parser.add_option('-5', '--renamecontainer', dest='renamecontainer', default='', help='rename existing container - args = %s' % (','.join(renameContainerArgs)))
		parser.add_option('-6', '--addcontainer', dest='addcontainer', default='', help='add container to parent container - args = %s' % (','.join(addContainerArgs)))
		parser.add_option('-7', '--dump', dest='dump', default='', help='dump workflows - args = %s' % (','.join(dumpWorkFlowArgs)))
		parser.add_option('-8', '--viewcontainer', dest='viewcontainer', default='', help='view container contents - args = %s' % (','.join(viewContainerArgs)))
		parser.add_option('-9', '--updatekv', dest='updatekv', default='', help='update key value pair - args = %s' % (','.join(updateKVArgs)))
		parser.add_option('-0', '--viewcodes', dest='viewcodes', default='', help='view all container codes & descriptions - args = %s' % (','.join(updateKVArgs)))

		return parser

	def run(self,options, args):
		connection = None
		try:
			connectionParms = dbConnParms.DbConnectionParms(options.host, options.port, options.dbname, options.user, options.password)
			connection = sqlUtilities.SqlUtilities(connectionParms)
			command = Command(connection, options, args)
			command.run()
		except Exception, e:
			print e.message
		finally:
			connection.closeMpsConnection()


if __name__ == '__main__':
	import MPSCore.utilities.sqlUtilities as sqlUtilities

	commandLineInterface = CommandLineInterface()
	parser = commandLineInterface.get_parser()
	(options, args) = parser.parse_args()
	commandLineInterface.run(options, args)

