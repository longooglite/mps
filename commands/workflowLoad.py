# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
load workflows from python files, convert to JSON and persist to wf_component

to merge, use: coreComponentDict.update(siteComponentOverrideDict)
'''
import json
import sys
import os
import os.path
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import logging
import logging.config
import optparse
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.core.constants
import cStringIO

kLoadTypeCore = "core"
kLoadTypeSite = "site"
kLoadTypeOverride = "override"


class WFLoad(object):
	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'mpsdev'
		self.user = 'mps'
		self.password = 'mps'
		self.db = None
		self.site = 'dev'

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.site: self.site = options.site.replace('-','_')

	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		try:
			self.connectToDatabase()
			self.fullReplace()
			siteImportSting = "from data.atramData.sites.%s.components%s import %s as currTask"
			self.loadComponents(True,siteImportSting)
			self.loadOverrides()
		except Exception, e:
			print e.message
			sys.exit(999)

	def fullReplace(self):
		sql = "delete from wf_component_override"
		self.db.executeSQLCommand(sql,())
		sql = "delete from wf_component"
		self.db.executeSQLCommand(sql,())

	def loadComponents(self,isSite, _importString):
		corePath = self.getComponentPath(kLoadTypeCore if not isSite else kLoadTypeSite)
		components = self.getComponentListing(corePath)
		try:
			for component in components:
				src = self.getSourceData(component.get('fullpath',''))
				componentName = component.get('filename','')[0:len(component.get('filename',''))-3]
				if isSite:
					importString = _importString % (self.site,component.get('subpath','')+componentName,componentName)
				else:
					importString = _importString % (componentName,componentName)
				relativeParts = component.get('fullpath','').split('atramData')
				CARRelativePath = relativeParts[1]
				exec importString
				taskCode = currTask.get('code','')
				taskDescr = currTask.get('descr','')
				metaTrackCodes = currTask.get("metaTrackCodes",None)
				jobActionType = currTask.get("jobActionType",None)
				if (metaTrackCodes and jobActionType):
					self.upsertWorkFlowAndMetaTrackAssociations(taskCode,taskDescr,metaTrackCodes,jobActionType)
				componentType = currTask.get('componentType','')
				if taskCode <> '':
					descr = currTask.get('descr','')
					self.upsertComponent(taskCode,descr,json.dumps(currTask),isSite,src,componentType,CARRelativePath)
		except Exception,e:
			print e.message
			sys.exit(999)


	def loadOverrides(self):
		overrideFiles = self.getComponentListing(self.getComponentPath(kLoadTypeOverride),True)
		if overrideFiles <> []:
			for overrideFile in overrideFiles:
				fileName = overrideFile.get('filename','')[0:len(overrideFile.get('filename',''))-3]
				overrideImportSting = "from data.atramData.sites.%s.components.overrides import %s as overrides" % (self.site,fileName)
				exec overrideImportSting
				for override in overrides.overrides:
					workflowCode = override.get('workflowCode','')
					titleCode = override.get('titleCode','')
					componentCode = override.get('componentCode','')
					self.upsertWorkFlowOverride(workflowCode,titleCode,componentCode,json.dumps(override))


	def getSourceData(self,componentPath):
		f = None
		try:
			f = open(componentPath,'rU')
			return f.read()
		except Exception,e:
			print "Unable to read src file %s" % (componentPath)
			for err in e.args:
				print err
			return ''
		finally:
			if f:
				f.close()

	def getComponentListing(self,path,loadOverrides = False):
		files = []
		for dirname, dirnames, filenames in os.walk(path):
			for filename in filenames:
				if not filename == "__init__.py" and filename.endswith(".py"):
					if (not dirname.endswith("overrides")) or (loadOverrides and dirname.endswith("overrides")):
						subparts = dirname.split(path)
						subpath = '.'
						if len(subparts) > 0 and subparts[1]:
							subpath = subparts[1].replace('/','.') + '.'
						files.append({"filename":filename,"fullpath":dirname + os.sep + filename,"subpath":subpath})
		return files

	def getComponentPath(self,pathRoot):
		carPath = os.path.abspath(__file__).split("car")[0] + "car" + os.sep
		corePath = "%sdata%satramData%s" % (carPath,os.sep,os.sep)
		path = ''
		if pathRoot == kLoadTypeCore:
			path = "%scomponents" % (corePath)
		elif pathRoot == kLoadTypeSite:
			path = "%ssites%s%s%scomponents" % (corePath,os.sep,self.site,os.sep)
		elif pathRoot == kLoadTypeOverride:
			path = "%ssites%s%s%scomponents%soverrides" % (corePath,os.sep,self.site,os.sep,os.sep)
		return path

	def upsertWorkFlowOverride(self,workflowCode,titleCode,componentCode,value):
		existingComponent = self.findTitleOverride(workflowCode,titleCode,componentCode)
		if existingComponent is None:
			self.insertComponentOverride(workflowCode,titleCode,componentCode,value)
		else:
			self.updateComponentOverride(existingComponent['id'],value)

	def findTitleOverride(self,workflowCode,titleCode,componentCode):
		sql = "SELECT * FROM wf_component_override WHERE workflow_code = %s AND component_code = %s AND title_code = %s "
		args = (workflowCode,componentCode,titleCode,)
		qry = self.db.executeSQLQuery(sql,args)
		if len(qry) > 0:
			return qry[0]
		return None

	def insertComponentOverride(self,workflowCode,titleCode,componentCode,value):
		sql = "INSERT INTO wf_component_override (workflow_code,component_code,title_code,value) VALUES (%s,%s,%s,%s)"
		args = (workflowCode,componentCode,titleCode,value)
		self.db.executeSQLCommand(sql,args)

	def updateComponentOverride(self,overrideId,value):
		sql = "UPDATE wf_component_override SET value = %s WHERE id = %s"
		args = (value,overrideId,)
		self.db.executeSQLCommand(sql,args)

	def upsertComponent(self, taskCode, descr, component, siteOverride, src, componentType,CARRelativePath):
		existingComponent = self.findComponent(taskCode,siteOverride)
		if existingComponent is None:
			self.insertComponent(taskCode, descr, component,siteOverride,src,componentType,CARRelativePath)
		else:
			self.updateComponent(existingComponent['id'], descr, component,siteOverride,src,CARRelativePath)

	def insertComponent(self,taskCode, descr, component,siteOverride,src,componentType,CARRelativePath):
		sql = "INSERT INTO wf_component (code, descr, value, is_site_override,src,car_relative_path,component_type_id) VALUES (%s,%s,%s,%s,%s,%s, (SELECT ID FROM wf_component_type WHERE upper(code) = UPPER(%s)))"
		args = (taskCode,descr,component,siteOverride,src,CARRelativePath,componentType,)
		self.db.executeSQLCommand(sql,args)

	def updateComponent(self,taskId, descr, component,siteOverride,src,CARRelativePath):
		sql = "UPDATE wf_component SET descr = %s,value = %s,is_site_override = %s,src = %s,car_relative_path = %s WHERE id = %s"
		args = (descr,component,siteOverride,src,CARRelativePath,taskId,)
		self.db.executeSQLCommand(sql,args)

	def upsertWorkFlowAndMetaTrackAssociations(self,wfCode,wfDescr,metaTrackCodes,jobActionType):
		wfid = self.findWFWorkflow(wfCode)
		if wfid:
			self.upsertWorkflow(wfCode,wfDescr,jobActionType)
		else:
			self.insertWorkflow(wfCode,wfDescr,jobActionType)
			wfid = self.findWFWorkflow(wfCode)
		self.insertWorkflowAndMetaTrack(wfid,metaTrackCodes)

	def insertWorkflowAndMetaTrack(self,wfid,metaTrackCodes):
		self.db.executeSQLCommand("DELETE FROM wf_workflow_metatrack WHERE workflow_id = %s",(wfid,))
		for meatTrackCode in metaTrackCodes:
			meatTrackId = self.getLookupTable("wf_metatrack",meatTrackCode)
			self.db.executeSQLCommand("INSERT INTO wf_workflow_metatrack (workflow_id,metatrack_id) VALUES (%s,%s)",(wfid,meatTrackId,))

	def upsertWorkflow(self,wfCode,wfDescr,jobActionTypeCode):
		sql = "UPDATE wf_workflow SET descr = %s,job_action_type_id = %s WHERE code = %s"
		jobActionTypeId = self.getLookupTable("wf_job_action_type",jobActionTypeCode)
		args = (wfDescr,jobActionTypeId,wfCode,)
		self.db.executeSQLCommand(sql,args)

	def insertWorkflow(self,wfCode,wfDescr,jobActionTypeCode):
		sql = "INSERT INTO wf_workflow (code,descr,job_action_type_id) VALUES (%s,%s,%s)"
		jobActionTypeId = self.getLookupTable("wf_job_action_type",jobActionTypeCode)
		args = (wfCode,wfDescr,jobActionTypeId,)
		self.db.executeSQLCommand(sql,args)

	def getLookupTable(self,_tableName, code):
		sql = "SELECT id FROM %s " % (_tableName)
		sql += "WHERE code = %s"
		args = (code,)
		qry = self.db.executeSQLQuery(sql,args)
		if qry:
			return qry[0]['id']
		return None

	def findWFWorkflow(self,code):
		sql = "SELECT id FROM wf_workflow WHERE code = %s"
		args = (code,)
		qry = self.db.executeSQLQuery(sql,args)
		if len(qry) > 0:
			return qry[0]['id']
		return None

	def findComponent(self,taskCode,siteOverride):
		sql = "SELECT * FROM wf_component WHERE code = %s AND is_site_override = %s"
		args = (taskCode,siteOverride)
		qry = self.db.executeSQLQuery(sql,args)
		if len(qry) > 0:
			return qry[0]
		return None

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)


class WFLoadInterface:
	DESCR = '''atram workflow load'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsdev', help='database name (default=mpsdev')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-s', '--site', dest='site', default='umms', help='folder in cvMetaData to load meta data from. Lookup data is the same across all sites.')

		return parser

	def run(self, options, args):
		wfLoad = None
		try:
			wfLoad = WFLoad(options, args)
			wfLoad.process()
		except Exception, e:
			print e.message
		finally:
			if wfLoad:
				wfLoad.shutdown()


if __name__ == '__main__':
	logging.config.fileConfig(cStringIO.StringIO(MPSCore.core.constants.kDebugFormatFile))
	import MPSCore.utilities.sqlUtilities as sqlUtilities

	dataLoadInterface = WFLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
	sys.exit(0)
