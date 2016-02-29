# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.jobActionService as  jobActionService
import MPSAppt.core.sql.itemInjectionSQL as injectionSQL
import MPSAppt.core.constants as constants
import json

class ItemInjectionService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getItemInjection(self,jobTaskId):
		return injectionSQL.getItemInjection(self.connection,jobTaskId)

	def addItemInjection(self,_jobTaskDict,_itemInjectionDict,doCommit=True):
		existingItemInjection = self.getItemInjection(_jobTaskDict.get('id',-1))
		try:
			if not existingItemInjection:
				injectionSQL.createItemInjection(self.connection, _itemInjectionDict, doCommit = False)
			else:
				injectionSQL.updateItemInjection(self.connection,_itemInjectionDict,doCommit = False)
			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def removeItemInjections(self,_itemInjectionDict,_container,_jobActionDict,jaSvc):
		injectionPossibilities = _container.getConfigDict().get('items',{})
		i = 1
		maxPossibilities = len(injectionPossibilities)
		while i <= maxPossibilities:
			key = 'set%i' % (i)
			i+=1
			taskCodesString = _itemInjectionDict.get('task_codes','')
			if taskCodesString:
				taskCodesToBeInjected = json.loads(taskCodesString)
				if not taskCodesToBeInjected.get(key,None):
					thisSet = injectionPossibilities.get(key,None)
					if thisSet:
						for aContainerCode in thisSet:
							sectionContainer = _container.workflow.getContainer(aContainerCode)
							for container in sectionContainer.getContainers():
								if container.containerDict.get('enabled',False):
									container.deleteYourself()



	def handleSubmit(self, _jobActionDict, _jobTaskDict, _itemInjectionDict, _container, _profile,doCommit = True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _itemInjectionDict.get('created','')
			logDict['lastuser'] = _itemInjectionDict.get('lastuser','')

			jaSvc = jobActionService.JobActionService(self.connection)
			self.removeItemInjections(_itemInjectionDict,_container,_jobActionDict,jaSvc)
			self.addItemInjection(_jobTaskDict, _itemInjectionDict, doCommit=False)
			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbPlaceholder
				logDict['item'] = 'entered'
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jaSvc.createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _itemInjectionDict.get('created',''), _itemInjectionDict.get('lastuser',''), doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e
