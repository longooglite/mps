# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
titleOverrides.py

#REQUIRED - need to load workflows prior to running roster load to ensure there is a new appointment job action in place.
'''

import sys
import os
import os.path
import csv
import json
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import logging
import logging.config
import optparse
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSAppt.services.workflowEditService as wfeditSvc
import MPSCore.core.constants
import cStringIO
import pprint
kDelimiter = "\t"


class TitleOverrides(object):

	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'mpsdev'
		self.user = 'mps'
		self.password = 'mps'
		self.db = None
		self.messageList = []
		self.site = 'dev'
		self.jobaction_type = 'Appointment'
		self.workflow_code = ''
		self.itemMap = 'itemMap.txt'

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.site: self.site = options.site
			if options.jobaction_type:self.jobaction_type = options.jobaction_type
			if options.workflow_code:self.workflow_code = options.workflow_code
			if options.item_map:self.itemMap = options.item_map
		self.site = self.site.replace('-','_')

	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		try:
			self.connectToDatabase()
			itemMap = self.getItemMap()
			fileData = self.getImportFileBySite("documents.txt")
			documentOverrides = self.parseDocsAndApprovals(fileData,itemMap)
			self.writeDocsApprovalsOverrides('uploadOverrides',documentOverrides)

			fileData = self.getImportFileBySite("approvals.txt")
			documentOverrides = self.parseDocsAndApprovals(fileData,itemMap)
			self.writeDocsApprovalsOverrides('approvalOverrides',documentOverrides)

			fileData = self.getImportFileBySite("acad_eval.txt")
			documentOverrides = self.parseAcadEvalAndSigPubs(fileData,itemMap,'acadeval')
			self.writeAcadEvalSigPubsOverrides('acadEvalOverrides',documentOverrides)

			fileData = self.getImportFileBySite("sig_pubs.txt")
			documentOverrides = self.parseAcadEvalAndSigPubs(fileData,itemMap,'sigpub')
			self.writeAcadEvalSigPubsOverrides('sigPubsOverrides',documentOverrides)

			fileData = self.getImportFileBySite("primary_rfp.txt")
			documentOverrides = self.parseRFPQuestions(fileData,itemMap)
			self.writePrimaryRFPOverrides('primaryRFPOverrides',documentOverrides)

		except Exception, e:
			print e.message

	def parseAcadEvalAndSigPubs(self,fileData,itemMap,itemIdentifier):
		rowCounter = 0
		title = ''
		track = ''
		workflowType = ''
		documents = []
		itemCode = ''
		for row in fileData:
			titleCode = ''
			rowCounter += 1
			columnCounter = 0
			titleDict = {}

			#column data
			isEnabled = False
			#acad eval
			numArmsLength = ''
			minFromChair = ''
			minRequired = ''
			#sig pubs
			min = ''
			max = ''

			for columnValue in row:
				columnCounter += 1

				if columnCounter == 1:
					title = columnValue
				elif columnCounter == 2:
					track = columnValue
				elif columnCounter == 3:
					workflowType = columnValue
				elif columnCounter == 4 and rowCounter == 1:
					itemDescr = columnValue
					itemCode = itemMap.get(itemDescr,'')
					if not itemCode:
						print "Unable to find item code for %s" % (columnValue)

				if columnCounter > 3 and rowCounter > 1:
					if workflowType == self.jobaction_type:
						titleCode = track.replace(' ','') + title.replace(' ','')
						if columnCounter == 4:
							isEnabled = self.convertColumnValueToSomthingThatMakesSense(columnValue)
						if itemIdentifier == 'acadeval':
							if columnCounter == 5:
								numArmsLength = columnValue
							elif columnCounter == 6:
								minFromChair = columnValue
							elif columnCounter == 7:
								minRequired = columnValue
								titleDict = self.getAcadEvalDict(itemCode,titleCode,isEnabled,numArmsLength,minFromChair,minRequired)
						else:
							if columnCounter == 4:
								min = columnValue
							elif columnCounter == 5:
								max = columnValue
								titleDict = self.getSigPubsDict(itemCode,titleCode,isEnabled,min,max)
			if titleDict:
				documents.append(titleDict)
		return documents

	def getAcadEvalDict(self,itemCode,titleCode,isEnabled,numArmsLength,minFromChair,minRequired):
		enabled = False
		configDict = {}
		if isEnabled == 'required':
			container = wfeditSvc.WorkflowService(self.db).getContainerDict(itemCode)
			enabled = True
			numArmsLength = numArmsLength
			minFromChair = minFromChair
			minRequired = minRequired
			configDict = {}
			containerList = container.get('config',{}).get('evaluatorSources',[])
			configDict["evaluatorSources"] = self.getConfigList(containerList,"CHAIR","min",minFromChair)
			configDict["min"] = minRequired
			#containerList = container.get('config',{}).get('evaluatorTypes',[])
			#configDict["evaluatorTypes"] = self.getConfigList(containerList,"AL_EXTERNAL","min",numArmsLength)
			containerList = container.get('config',{}).get('evaluatorTypeCollections',[])
			configDict["evaluatorTypeCollections"] = self.getEvaluatorTypeCollections(containerList,numArmsLength,["AL_EXTERNAL","AL_INTERNAL"])

		return {"componentCode":itemCode,"titleCode":titleCode,"workflowCode":self.workflow_code,"enabled":enabled,"config":configDict}


	def getEvaluatorTypeCollections(self,evaluatorTypeCollections,numArmsLength,codes):
		new_list = list(evaluatorTypeCollections)
		for collection in new_list:
			foundCollection = True
			for code in codes:
				if not code in collection.get('codes',[]):
					foundCollection = False
			if foundCollection:
				collection['min'] = numArmsLength
		return new_list


	def getConfigList(self,containerList,listItemCode,attributeKey,attributeValue):
		newList = []
		for each in containerList:
			newItem = each.copy()
			if newItem.get('code','') == listItemCode:
				newItem[attributeKey] = attributeValue
			newList.append(newItem)
		return newList

		#[{"code":"CHAIR","min":minFromChair}]

	def getSigPubsDict(self,itemCode,titleCode,isEnabled,min,max):
		enabled = False
		if isEnabled == 'required':
			enabled = True
		returnVal = {"componentCode":itemCode,"titleCode":titleCode,"workflowCode":self.workflow_code,"enabled":enabled}
		if enabled:
			configDict = {"config":{"min":self.getInt(min),"max":self.getInt(max)}}
			returnVal['config'] = configDict
		return returnVal

	def getInt(self,strValue):
		returnVal = 0
		try:
			returnVal = int(strValue)
		except:
			pass
		return returnVal

	def parseDocsAndApprovals(self,fileData,itemMap):
		rowCounter = 0
		title = ''
		track = ''
		workflowType = ''
		documents = []
		titleDict = {}
		for row in fileData:
			titleCode = ''
			if titleDict:
				documents.append(titleDict)
			rowCounter += 1
			if rowCounter > 1:
				titleDict = {"titleCode":"","itemList":[]}
			columnCounter = 0
			for columnValue in row:
				if columnCounter == 0:
					title = columnValue
				elif columnCounter == 1:
					track = columnValue
				elif columnCounter == 2:
					workflowType = columnValue
				columnCounter += 1
				if columnCounter > 3:
					if rowCounter == 1:
						itemCode = itemMap.get(columnValue,'')
						if not itemCode:
							print "Unable to find item code for %s" % (columnValue)
						else:
							itemMap[columnCounter] = itemCode
					else:
						itemCode = itemMap.get(columnCounter,'')
						if itemCode:
							if not titleCode:
								titleCode = track.replace(' ','') + title.replace(' ','')
								titleDict['titleCode'] = titleCode
							columnValue = self.convertColumnValueToSomthingThatMakesSense(columnValue)
							titleDict['itemList'].append({"item":itemCode,"value":columnValue,"workflowType":workflowType})
		if titleDict:
			documents.append(titleDict)
		return documents

	def parseRFPQuestions(self,fileData,itemMap):
		documents = []
		questionMap = {}
		if self.jobaction_type == 'Promotion':
			#   There are no RFP overrides for Promotion
			return documents

		rowCounter = 0
		for row in fileData:
			rowCounter += 1
			if rowCounter == 1:
				# ignore first row, simply the text of the RFP questions
				continue

			if rowCounter == 2:
				# 2nd row, map Ringo's question code to our question code
				columnCounter = 0
				for columnValue in row:
					columnCounter += 1
					if columnCounter > 3:
						internalQuestionCode = itemMap.get(str(columnValue), '')
						if not internalQuestionCode:
							print "Unable to find internal question code for %s" % (columnValue)
						else:
							questionMap[columnCounter] = internalQuestionCode
				continue

			#   rows 3+ are data rows
			workflowType = row[2]
			if workflowType == self.jobaction_type:
				omitCodes = []
				columnCounter = 0
				for columnValue in row:
					columnCounter += 1
					if columnCounter > 3:
						internalQuestionCode = questionMap.get(columnCounter,'')
						if internalQuestionCode:
							convertedColumnValue = self.convertColumnValueToSomthingThatMakesSense(columnValue)
							if convertedColumnValue != 'required':
								omitCodes.append(internalQuestionCode)
				if omitCodes:
					containerDict = wfeditSvc.WorkflowService(self.db).getContainerDict('rfp')
					if containerDict:
						configDict = containerDict.get('config', {})
						configDict['omitCodes'] = json.dumps(omitCodes)

						title = row[0]
						track = row[1]
						titleCode = track.replace(' ','') + title.replace(' ','')
						titleDict = {}
						titleDict['titleCode'] = titleCode
						titleDict['itemList'] = [{ "item": "rfp", "value": configDict, "workflowType": workflowType }]
						documents.append(titleDict)

		return documents


	def writeDocsApprovalsOverrides(self,outputFileName,documentOverrides):
		titlesNotFound = []
		containersNotFound = []
		wfedit = wfeditSvc.WorkflowService(self.db)
		overrideDictList = []
		for override in documentOverrides:
			titleCode = override.get('titleCode','')
			if titleCode:
				title = self.getTitle(titleCode)
				if not title:
					titlesNotFound.append(titleCode)
				else:
					for each in override.get('itemList',[]):
						if each.get('workflowType','') == self.jobaction_type:
							container = wfedit.getContainerDict(each.get('item',{}))
							if not container:
								containersNotFound.append(each.get('item',''))
							else:
								overrideValue = each.get('value','notfound')
								overrideDict = {"workflowCode":self.workflow_code,"componentCode":container['code'],"titleCode":titleCode}
								if overrideValue <> 'notfound':
									doOverride = False
									if overrideValue == 'optional' and container.get('optional',True) == False:
										overrideDict['optional'] = True
										doOverride = True
									elif overrideValue == 'required' and container.get('optional',True) == True:
										overrideDict['optional'] = False
										doOverride = True
									elif overrideValue == 'disabled':
										overrideDict['enabled'] = False
										doOverride = True
									if doOverride:
										overrideDictList.append(overrideDict)
		self.writeTitleOverrideDict(overrideDictList,outputFileName)


	def writeAcadEvalSigPubsOverrides(self,outputFileName,documentOverrides):
		titlesNotFound = []
		containersNotFound = []
		wfedit = wfeditSvc.WorkflowService(self.db)
		overrideDictList = []
		for override in documentOverrides:
			titleCode = override.get('titleCode','')
			if titleCode:
				title = self.getTitle(titleCode)
				if not title:
					titlesNotFound.append(titleCode)
				else:
					container = wfedit.getContainerDict(override.get('componentCode',{}))
					if not container:
						containersNotFound.append(override.get('componentCode',''))
					else:
						if override.get('componentCode','') == 'acad_eval':
							shouldAppend = self.validateAcadEval(container,override)
						else:
							shouldAppend = self.validateSigPubs(container,override)
						if shouldAppend:
							overrideDictList.append(override)
		self.writeTitleOverrideDict(overrideDictList,outputFileName)


	def writePrimaryRFPOverrides(self,outputFileName,documentOverrides):
		titlesNotFound = []
		containersNotFound = []
		wfedit = wfeditSvc.WorkflowService(self.db)
		overrideDictList = []
		for override in documentOverrides:
			titleCode = override.get('titleCode','')
			if titleCode:
				title = self.getTitle(titleCode)
				if not title:
					titlesNotFound.append(titleCode)
				else:
					for each in override.get('itemList',[]):
						if each.get('workflowType','') == self.jobaction_type:
							container = wfedit.getContainerDict(each.get('item',{}))
							if not container:
								containersNotFound.append(each.get('item',''))
							else:
								overrideValue = each.get('value', {})
								if overrideValue:
									overrideDict = {}
									overrideDict['workflowCode'] = self.workflow_code
									overrideDict['componentCode'] = container['code']
									overrideDict['titleCode'] = titleCode
									overrideDict['config'] = overrideValue
									overrideDictList.append(overrideDict)

		self.writeTitleOverrideDict(overrideDictList,outputFileName)


	def validateAcadEval(self,container,override):
		if not override.get('enabled',True):
			return True
		overrideConfig = override.get('config',{})
		containerConfig = container.get('config',{})
		if overrideConfig.get('min','') <> containerConfig.get('min',''):
			return True
		overrideSources = overrideConfig.get('evaluatorSources',[])
		overrideChairDict = {}
		for each in overrideSources:
			if each.get('code','') == 'CHAIR':
				overrideChairDict = each
				break
		containerSources = containerConfig.get('evaluatorSources',[])
		containerChairDict = {}
		for each in containerSources:
			if each.get('code','') == 'CHAIR':
				containerChairDict = each
				break
		if containerChairDict.get('min','') <> overrideChairDict.get('min',''):
			return True
		overrideTypes = overrideConfig.get('evaluatorTypes',[])
		overrideTypeDict = {}
		for each in overrideTypes:
			if each.get('code','') == 'AL_EXTERNAL':
				overrideTypeDict = each
				break
		containerTypes = containerConfig.get('evaluatorTypes',[])
		containerTypeDict = {}
		for each in containerTypes:
			if each.get('code','') == 'AL_EXTERNAL':
				containerTypeDict = each
				break
		if containerTypeDict.get('min','') <> overrideTypeDict.get('min',''):
			return True
		return False

	def validateSigPubs(self,container,override):
		if not override.get('enabled',True):
			return True
		overrideConfig = override.get('config',{})
		containerConfig = container.get('config',{})
		if overrideConfig.get('min','') <> containerConfig.get('min',""):
			return True
		if overrideConfig.get('max','') <> containerConfig.get('max',""):
			return True
		return False

	def convertColumnValueToSomthingThatMakesSense(self,inbound):
		if inbound.upper() == 'YES':
			return 'required'
		elif inbound.upper() == 'OPTIONAL':
			return 'optional'
		elif inbound.upper() == 'NA':
			return 'disabled'
		else:
			return 'disabled'

	def writeTitleOverrideDict(self,overrideDictList,outputFileName):
		try:
			folderPath = os.path.expanduser("~/Desktop/") + "overrides/"
			filePath = folderPath + "%s.py" % (outputFileName)
			if not os.path.exists(folderPath):
				os.makedirs(folderPath)
			f = open(filePath,'w')
			f.write("overrides=")
			pprint.pprint(overrideDictList,f)
			f.flush()
			f.close()
		except Exception,e:
			pass


	def getTitle(self,titleCode):
		sql = "select * from wf_title where upper(code) = %s"
		args = (titleCode.upper(),)
		qry = self.db.executeSQLQuery(sql,args)
		if qry:
			return qry[0]
		return None


	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)

	def getSiteFilePath(self,fileName):
		return os.path.abspath(__file__).split("car")[0] + "car%sdata%satramData%ssites%s%s%s" % (os.sep,os.sep,os.sep,os.sep,self.site,os.sep) + fileName

	def getFilePath(self,fileName):
		return os.path.abspath(__file__).split("car")[0] + "car%sdata%satramData%s" % (os.sep,os.sep,os.sep) + fileName

	def getItemMap(self):
		f = open(self.getSiteFilePath(self.itemMap))
		contents = f.read()
		map = json.loads(contents)
		return map

	def getImportFileBySite(self, fileName):
		filepath = self.getSiteFilePath(fileName)
		f = open(filepath, 'rU')
		data = list(csv.reader(f, delimiter='\t'))
		f.close()
		return data

	def getImportFile(self, fileName):
		filepath = self.getFilePath(fileName)
		f = open(filepath, 'rU')
		data = list(csv.reader(f, delimiter='\t'))
		f.close()
		return data



class DataLoadInterface:
	DESCR = '''Data Load for Title Overrides.'''

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
		parser.add_option('-j', '--jobaction_type', dest='jobaction_type', default='Appointment', help='Appointment, Promotion, or Reappointment')
		parser.add_option('-c', '--workflow_code', dest='workflow_code', default='umms_appoint_workflow', help='workflow code')
		parser.add_option('-m', '--item_map', dest='item_map', default='itemMap.txt', help='which item map file to use')
		return parser

	def run(self, options, args):
		atramLoad = None
		try:
			atramLoad = TitleOverrides(options, args)
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
