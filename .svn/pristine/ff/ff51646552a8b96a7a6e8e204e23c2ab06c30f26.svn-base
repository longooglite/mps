# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.uberSQL as uberSQL
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.personService as personSvc
from MPSCore.handlers.coreApplicationHandler import globalRequestData

kElementTypeQuestion = 'question'
kElementTypeGroup = 'group'

kQuestionTypeText = 'TEXT'
kQuestionTypeTextArea = 'TEXTAREA'
kQuestionTypeRepeatingText = 'REPEATING_TEXT'
kQuestionTypeRadio = 'RADIO'
kQuestionTypeCheckbox = 'CHECKBOX'
kQuestionTypeDropdown = 'DROPDOWN'
kQuestionTypeMultiDropdown = 'MULTI_DROPDOWN'
kQuestionTypeDate = 'DATE'

class UberService(AbstractTaskService):

	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)
		self.questionCache = {}
		self.groupCache = {}
		self.omittedQuestionAndGroupCodes = []  #   a List of Group and/or Question codes that should be omitted,
												#   i.e. treated as though they don't even exist. Set by the calling
												#   program after object instantiation, if appropriate.
		self.jobActionTypeCodes = []            #   Job Action Type codes relevant to the associated Job Action.
												#   When assembling the list of applicable questions, this value is
												#   used as a filter to screen out inapplicable questions.
												#   Set by the calling program after object instantiation, if appropriate.

	def getOmittedQuestionAndGroupCodes(self): return self.omittedQuestionAndGroupCodes
	def setOmittedQuestionAndGroupCodes(self, _omittedQuestionAndGroupCodes): self.omittedQuestionAndGroupCodes = _omittedQuestionAndGroupCodes

	def getJobActionTypeCodes(self): return self.jobActionTypeCodes
	def setJobActionTypeCodes(self, _jobActionTypeCodes): self.jobActionTypeCodes = _jobActionTypeCodes

	#   Simple queries.

	def getUberGroups(self):
		if 'uberGroups' not in globalRequestData:
			globalRequestData['uberGroups'] = uberSQL.getUberGroups(self.connection)
		return globalRequestData.get('uberGroups', [])

	def getUberQuestions(self):
		if 'uberQuestions' not in globalRequestData:
			globalRequestData['uberQuestions'] = uberSQL.getUberQuestions(self.connection)
		return globalRequestData.get('uberQuestions', [])

	def getUberOptions(self):
		if 'uberOptions' not in globalRequestData:
			globalRequestData['uberOptions'] = uberSQL.getUberOptions(self.connection)
		return globalRequestData.get('uberOptions', [])

	def getUberOptionsForQuestion(self, _questionDict):
		return uberSQL.getUberOptionsForQuestion(self.connection, _questionDict)

	def getUber(self, _jobTaskId):
		return lookupTableSvc.getEntityByKey(self.connection, 'wf_uber', _jobTaskId, _key='job_task_id')

	def getUberResponses(self, _jobTaskId):
		result = {}
		rawList = lookupTableSvc.getEntityListByKey(self.connection, 'wf_uber_response', _jobTaskId, _key='job_task_id', _orderBy='question_code,repeat_seq')
		for row in rawList:
			questionCode = row.get('question_code','')
			if questionCode:
				if questionCode not in result:
					result[questionCode] = []
				result[questionCode].append(row)
		return result

	def getUberSavedSet(self, _uberGroupId):
		uberSavedSet = uberSQL.getUberSavedSet(self.connection, _uberGroupId)
		if uberSavedSet:
			uberSavedSet['items'] = uberSQL.getUberSavedSetItemsForSavedSetId(self.connection, _uberGroupId)
		return uberSavedSet

	def getUberSavedSetNames(self, _community, _username, _uberGroupCode):
		return uberSQL.getUberSavedSetNames(self.connection, _community, _username, _uberGroupCode)

	def matchUberSavedSetByDescr(self, _community, _username, _descr):
		return uberSQL.matchUberSavedSetByDescr(self.connection, _community, _username, _descr)


	#   Simple CRUD.

	def createUber(self, _uberDict, doCommit=True):
		uberSQL.createUber(self.connection, _uberDict, doCommit)

	def updateUberJson(self, _uberDict, doCommit=True):
		uberSQL.updateUberJson(self.connection, _uberDict, doCommit)

	def updateUberComplete(self, _uberDict, doCommit=True):
		uberSQL.updateUberComplete(self.connection, _uberDict, doCommit)

	def deleteUberResponsesForTask(self, _jobTaskDict, doCommit=True):
		uberSQL.deleteUberResponsesForTask(self.connection, _jobTaskDict, doCommit)

	def createUberSavedSet(self, _uberSavedSetDict, doCommit=True):
		return uberSQL.createUberSavedSet(self.connection, _uberSavedSetDict, doCommit)

	def createUberSavedSetItem(self, _uberSavedSetItemDict, doCommit=True):
		return uberSQL.createUberSavedSetItem(self.connection, _uberSavedSetItemDict, doCommit)

	def deleteUberSavedSet(self, _uberSavedSetId, doCommit=True):
		try:
			self.deleteUberSavedSetItemsForSavedSetId(_uberSavedSetId, doCommit=False)
			uberSQL.deleteUberSavedSet(self.connection, _uberSavedSetId, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def deleteUberSavedSetItemsForSavedSetId(self, _uberSavedSetId, doCommit=True):
		uberSQL.deleteUberSavedSetItemsForSavedSetId(self.connection, _uberSavedSetId, doCommit)


	#   Build a question set.

	def assembleUberQuestionSet(self, _uberGroupCode):
		self.questionCache = self.getUberQuestionCache()
		self.groupCache = self.getUberGroupCache()
		self.identifyQuestionsInRepeatingGroups()
		self.identifyRepeatingGroupsManagedByTables()
		self.identifyConditionalTargets()

		if _uberGroupCode in self.groupCache:
			return self.buildUberElement(_uberGroupCode)
		return {}

	def buildUberElement(self, _uberGroupOrQuestionCode):
		if _uberGroupOrQuestionCode in self.questionCache:
			return self.questionCache[_uberGroupOrQuestionCode]

		if _uberGroupOrQuestionCode in self.groupCache:
			uberGroup = self.groupCache[_uberGroupOrQuestionCode]
			uberGroup['elements'] = []
			children = uberGroup.get('children', '')
			childrenCodes = children.split(',')
			for code in childrenCodes:
				child = self.buildUberElement(code)
				if child:
					uberGroup['elements'].append(child)
			return uberGroup

		return None


	#   Event Handlers.

	def handleSubmit(self, _jobActionDict, _jobTaskDict, _insertList, _updateList, _deleteList, _container, _isDraft, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update/Delete rows in the Uber Response table.
			for uberResponseDict in _deleteList:
				uberSQL.deleteUberResponse(self.connection, uberResponseDict, doCommit=False)
			for uberResponseDict in _updateList:
				uberSQL.updateUberResponse(self.connection, uberResponseDict, doCommit=False)
			for uberResponseDict in _insertList:
				uberSQL.createUberResponse(self.connection, uberResponseDict, doCommit=False)

			#   Update complete flag on Uber record.
			uberDict = {}
			uberDict['job_task_id'] = _jobTaskDict.get('id', 0)
			uberDict['complete'] = not _isDraft
			uberDict['updated'] = _now
			uberDict['lastuser'] = _username
			self.updateUberComplete(uberDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbUberFormDraft if _isDraft else constants.kJobActionLogVerbUberForm
				logDict['item'] = _container.getClassName()
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			activityLogConfigKeyName = 'draftActivityLog' if _isDraft else 'submitActivityLog'
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username, _activityLogConfigKeyName=activityLogConfigKeyName, doCommit=False)
			if not _isDraft:
				self.syncToPerson(_jobActionDict, _jobTaskDict, _container)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def syncToPerson(self, _jobActionDict, _jobTaskDict, _container):
		#   Sync wf_person information, if applicable.
		if not _container.getConfigDict().get('isPersonalInfo', False): return

		identifierCodes = _container.getConfigDict().get('personalInfoCodes', [])
		if not identifierCodes: return

		personDict = _container.getPersonDict()
		if not personDict: return

		_container.applyResponses()
		questionsByIdentifierCodeCache = _container.organizeQuestionsByIdentifierCode()
		for identifierCode in identifierCodes:
			questionDict = questionsByIdentifierCodeCache.get(identifierCode, {})
			if questionDict:
				responseList = questionDict.get('responseList', [])
				if responseList:
					thisResponseDict = responseList[0]
					personDict[identifierCode] = thisResponseDict.get('response', '')
				else:
					personDict[identifierCode] = ''

		personSvc.PersonService(self.connection).createOrUpdatePerson(_jobTaskDict, personDict, doCommit=False)

	def handleCreateSavedSet(self, _jobActionDict, _jobTaskDict, _savedSetDict, _savedSetItemList, _container, _profile, _now, _community, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Delete any existing Saved Set for this _username which 'matches' the name of the Saved Set we are trying to save.
			existingSavedSetList = self.matchUberSavedSetByDescr(_community, _username, _savedSetDict.get('descr', ''))
			if existingSavedSetList:
				savedSetId = existingSavedSetList[0].get('id', 0)
				self.deleteUberSavedSet(savedSetId, doCommit=False)

			#   Create rows in the Saved Set and Saved Set Items tables.
			newSavedSetId = self.createUberSavedSet(_savedSetDict, doCommit=False)
			for each in _savedSetItemList:
				each['saved_set_id'] = newSavedSetId
				self.createUberSavedSetItem(each, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbUberFormCreateSavedSet
				logDict['item'] = "%s %s" % (_container.getClassName(), _savedSetDict.get('descr', ''))
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			activityLogConfigKeyName = 'savedSetsCreateActivityLog'
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username, _activityLogConfigKeyName=activityLogConfigKeyName, _freezeConfigKeyName='', _dashboardConfigKeyName='', _alertConfigKeyName='', doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleApplySavedSet(self, _jobActionDict, _jobTaskDict, _savedSetDict, _container, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Delete any existing responses for this Uber form.
			self.deleteUberResponsesForTask(_jobTaskDict, doCommit=False)

			#   Transform Saved Set Items rows into Response records and persist.

			jobTaskId = _jobTaskDict.get('id', None)
			for itemDict in _savedSetDict.get('items', []):
				responseDict = {}
				responseDict['job_task_id'] = jobTaskId
				responseDict['question_code'] = itemDict.get('question_code', '')
				responseDict['repeat_seq'] = itemDict.get('repeat_seq', 0)
				responseDict['response'] = itemDict.get('response', '')
				responseDict['revisions_required'] = False
				responseDict['revisions_required_date'] = ''
				responseDict['revisions_required_comment'] = ''
				responseDict['created'] = _now
				responseDict['updated'] = _now
				responseDict['lastuser'] = _username
				uberSQL.createUberResponse(self.connection, responseDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbUberFormApplySavedSet
				logDict['item'] = "%s %s" % (_container.getClassName(), _savedSetDict.get('descr', ''))
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			activityLogConfigKeyName = 'savedSetsApplyActivityLog'
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username, _activityLogConfigKeyName=activityLogConfigKeyName, _freezeConfigKeyName='', _dashboardConfigKeyName='', _alertConfigKeyName='', doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleDeleteSavedSet(self, _jobActionDict, _jobTaskDict, _savedSetDict, _container, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Delete the specified Saved Set.
			savedSetId = _savedSetDict.get('id', 0)
			self.deleteUberSavedSet(savedSetId, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbUberFormDeleteSavedSet
				logDict['item'] = "%s %s" % (_container.getClassName(), _savedSetDict.get('descr', ''))
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			activityLogConfigKeyName = 'savedSetsDeleteActivityLog'
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username, _activityLogConfigKeyName=activityLogConfigKeyName, _freezeConfigKeyName='', _dashboardConfigKeyName='', _alertConfigKeyName='', doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e


	#   Admin event handlers.

	def saveQuestionAndOptions(self, _questionDict, _optionList, _isEdit, doCommit=True):
		try:
			if _isEdit:
				uberSQL.updateQuestion(self.connection, _questionDict, doCommit=False)
				uberSQL.removeUberOptionsForQuestion(self.connection, _questionDict, doCommit=False)
			else:
				uberSQL.createQuestion(self.connection, _questionDict, doCommit=False)
				_questionDict['id'] = self.connection.getLastSequenceNbr('wf_uber_question')

			questionId = _questionDict.get('id', 0)
			for optionDict in _optionList:
				optionDict['uber_question_id'] = questionId
				uberSQL.createOption(self.connection, optionDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def saveGroup(self, _groupDict, _isEdit, doCommit=True):
		try:
			if _isEdit:
				uberSQL.updateGroup(self.connection, _groupDict, doCommit=False)
			else:
				uberSQL.createGroup(self.connection, _groupDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e


	#   Cache builders.

	def getUberQuestionCache(self):

		#   Returns a dictionary of Uber Questions.
		#   key:    wf_uber_question.code
		#   value:  wf_uber_question row, with attached Options

		cache = {}
		optionsCache = self.getUberOptionCache()
		for uberQuestionDict in self.getUberQuestions():
			thisCode = uberQuestionDict.get('code', '')
			if thisCode:
				if thisCode not in self.getOmittedQuestionAndGroupCodes():
					shouldCache = False
					if not self.getJobActionTypeCodes():
						shouldCache = True
					else:
						questionTypesStr = uberQuestionDict.get('job_action_types', '')
						for typeCode in self.getJobActionTypeCodes():
							if typeCode in questionTypesStr:
								shouldCache = True

					if shouldCache:
						uberQuestionDict['type'] = kElementTypeQuestion
						uberQuestionDict['repeating'] = False
						uberQuestionDict['data_type'] = uberQuestionDict.get('data_type', '').upper()
						self.getConsolidatedOptionsForQuestion(uberQuestionDict, optionsCache)
						cache[thisCode] = uberQuestionDict
		return cache

	def getConsolidatedOptionsForQuestion(self, _uberQuestionDict, _optionsCache):

		#   For Dropdowns, the list of options can be specified in the wf_uber_option table (just like
		#   Radio Button controls), or can be specified as a reference to a static lookup table (such
		#   as STATES or COUNTRIES), or BOTH! When both are specified, the entries from the wf_uber_option
		#   table are treated as overrides to the entries from the static lookup table, and are arbitrarily
		#   positioned at the end of the option list.

		standardOptionsList = _optionsCache.get(_uberQuestionDict.get('id', 0), [])

		datatype = _uberQuestionDict.get('data_type', '')
		if (datatype == kQuestionTypeDropdown) or (datatype == kQuestionTypeMultiDropdown):
			uberQuestionCode = _uberQuestionDict.get('code', '')
			lookupKey = _uberQuestionDict.get('data_type_attributes', '')
			if lookupKey:
				if 'uberStaticCodeDescrCache' not in globalRequestData:
					globalRequestData['uberStaticCodeDescrCache'] = lookupTableSvc.getStaticCodeDescrCache(self.connection)
				lookupList = globalRequestData.get('uberStaticCodeDescrCache', {}).get(lookupKey, [])
				_uberQuestionDict['options'] = []
				for each in lookupList:
					optionDict = {}
					optionDict['code'] = "%s|%s" % (uberQuestionCode, each.get('code', ''))
					optionDict['display_text'] = each.get('descr', '')
					_uberQuestionDict['options'].append(optionDict)

				standardShowCodes = []
				for optionDict in standardOptionsList:
					optionShowCodes = optionDict.get('show_codes', '')
					showSplits = optionShowCodes.split(',')
					for oneCode in showSplits:
						if oneCode not in standardShowCodes:
							standardShowCodes.append(oneCode)
				lookupHideCodes = ",".join(standardShowCodes)

				for optionDict in standardOptionsList:
					gotIt = False
					optionCode = optionDict.get('code', '')
					if optionCode:
						for lookupOptionDict in _uberQuestionDict['options']:
							if optionCode == lookupOptionDict.get('code', ''):
								lookupOptionDict.update(optionDict)
								gotIt = True
							else:
								if 'hide_codes' not in lookupOptionDict:
									lookupOptionDict['hide_codes'] = lookupHideCodes
						if not gotIt:
							_uberQuestionDict['options'].append(optionDict)
			else:
				_uberQuestionDict['options'] = standardOptionsList
		else:
			_uberQuestionDict['options'] = standardOptionsList

	def getUberOptionCache(self):

		#   Returns a dictionary of consolidated Uber Option rows.
		#   key:    uber_question_id
		#   value:  list of associated wf_uber_option rows, in ascending seq order

		cache = {}
		prevKey = None
		curList = None
		for uberOptionDict in self.getUberOptions():
			thisKey = uberOptionDict.get('uber_question_id', 0)
			if thisKey:
				if thisKey != prevKey:
					prevKey = thisKey
					curList = []
					cache[thisKey] = curList
				curList.append(uberOptionDict)
		return cache

	def getUberGroupCache(self):

		#   Returns a dictionary of Uber Groups.
		#   key:    wf_uber_group.code
		#   value:  wf_uber_group row

		cache = {}
		for uberGroupDict in self.getUberGroups():
			thisCode = uberGroupDict.get('code', '')
			if thisCode:
				if thisCode not in self.getOmittedQuestionAndGroupCodes():
					uberGroupDict['type'] = kElementTypeGroup
					cache[thisCode] = uberGroupDict
		return cache

	def identifyQuestionsInRepeatingGroups(self):
		for groupCode in self.groupCache.keys():
			uberGroupDict = self.groupCache[groupCode]
			if uberGroupDict.get('repeating', False):
				children = uberGroupDict.get('children', '')
				childrenCodes = children.split(',')
				for code in childrenCodes:
					if code in self.questionCache:
						self.questionCache[code]['repeating'] = True

	def identifyRepeatingGroupsManagedByTables(self):
		tableGroups = self.extractTableGroups()
		if not tableGroups: return

		repeatingGroups = self.extractRepeatingGroups()
		if not repeatingGroups: return

		for tableGroupDict in tableGroups:
			self.findAndAssociateTableWithRepeatingGroup(tableGroupDict, repeatingGroups)

	def findAndAssociateTableWithRepeatingGroup(self, _tableGroupDict, _repeatingGroupList):
		tableGroupCode = _tableGroupDict.get('code', '')
		tableGroupChildren = _tableGroupDict.get('children', '')
		tableGroupChildrenCodes = tableGroupChildren.split(',')

		for repeatingGroupDict in _repeatingGroupList:
			if not repeatingGroupDict.get('managedByCode', ''):
				repeatingGroupChildren = repeatingGroupDict.get('children', '')
				repeatingGroupChildrenCodes = repeatingGroupChildren.split(',')

				for tableCode in tableGroupChildrenCodes:
					if tableCode in repeatingGroupChildrenCodes:
						repeatingGroupCode = repeatingGroupDict.get('code', '')
						repeatingGroupDict['managedByCode'] = tableGroupCode
						_tableGroupDict['managesGroupCode'] = repeatingGroupCode
						return

	def identifyConditionalTargets(self):
		for questionCode in self.questionCache.keys():
			uberQuestionDict = self.questionCache[questionCode]
			showCodes = uberQuestionDict.get('show_codes', '').split(',')
			for code in showCodes:
				childQuestion = self.questionCache.get(code, {})
				if childQuestion:
					if 'parentList' not in childQuestion:
						childQuestion['parentList'] = []
					if questionCode not in childQuestion['parentList']:
						childQuestion['parentList'].append(questionCode)

				childGroup = self.groupCache.get(code, {})
				if childGroup:
					if 'parentList' not in childGroup:
						childGroup['parentList'] = []
					if questionCode not in childGroup['parentList']:
						childGroup['parentList'].append(questionCode)

			for uberOptionDict in uberQuestionDict.get('options', []):
				optionCode = uberOptionDict.get('code', '')
				showCodes = uberOptionDict.get('show_codes', '').split(',')
				for code in showCodes:
					childQuestion = self.questionCache.get(code, {})
					if childQuestion:
						if 'parentList' not in childQuestion:
							childQuestion['parentList'] = []
						if optionCode not in childQuestion['parentList']:
							childQuestion['parentList'].append(optionCode)

					childGroup = self.groupCache.get(code, {})
					if childGroup:
						if 'parentList' not in childGroup:
							childGroup['parentList'] = []
						if optionCode not in childGroup['parentList']:
							childGroup['parentList'].append(optionCode)

	def extractRepeatingGroups(self):
		return self._extractGroups('repeating')

	def extractTableGroups(self):
		return self._extractGroups('repeating_table')

	def _extractGroups(self, _attributeName):
		desiredGroups = []
		for groupCode in self.groupCache.keys():
			uberGroupDict = self.groupCache[groupCode]
			if uberGroupDict.get(_attributeName, False):
				desiredGroups.append(uberGroupDict)
		return desiredGroups

	def getIsWaived(self, _container, _waiverQuestionCode, _waiverAffirmativeResponse):
		_container.loadInstance()
		responseList = _container.getUberInstance().get('responses', {}).get(_waiverQuestionCode, [])
		if responseList:
			answer = responseList[0].get('response', '')
			if answer == _waiverAffirmativeResponse:
				return True
		return False
