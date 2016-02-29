# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.core.constants as constants
import MPSAppt.core.sql.personSQL as personSQL
import MPSAppt.services.jobActionService as jobActionSvc

class PersonService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getPerson(self, _personId):
		return personSQL.getPerson(self.connection, _personId)

	def getPersonByCommunityUserName(self, _community, _username):
		return personSQL.getPersonByCommunityUserName(self.connection, { 'community': _community, 'username': _username })

	def createPerson(self, _personDict, doCommit=True):
		personSQL.createPerson(self.connection, _personDict, doCommit)

	def updatePerson(self, _personDict, doCommit=True):
		personSQL.updatePerson(self.connection, _personDict, doCommit)

	def createOrUpdatePerson(self, _jobTaskDict, _personDict, doCommit=True, now='', username=''):
		jaService = jobActionSvc.JobActionService(self.connection)
		try:
			personDict = self.uniquifyPerson(_personDict,_jobTaskDict,now,username)
			personId = personDict.get('id', -1)
			if personId > 0:
				self.updatePerson(personDict, doCommit=False)
			else:
				self.createPerson(personDict, doCommit=False)
				personId = self.connection.getLastSequenceNbr('wf_person')
			jaService.associatePersonWithJobAction(_jobTaskDict.get('job_action_id', None), personId, personDict.get('updated',None),  personDict.get('lastuser',None), doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def uniquifyPerson(self,_personDict,_jobTaskDict,now,username):
		if _personDict.get('username',''):
			_personDict['community'] = _personDict.get('community', 'default')
			#this is the case where a person is entered without a uniquname
			lastPersonEnteredDict = personSQL.getPerson(self.connection,_personDict.get('id',-1))
			if lastPersonEnteredDict:
				if not lastPersonEnteredDict.get('username',''):
					personByUniqueNameDict = personSQL.getPersonByCommunityUserName(self.connection,_personDict)
					if personByUniqueNameDict:
						self.resetPersonPointers(_personDict,personByUniqueNameDict,_jobTaskDict,now,username)
						community = personByUniqueNameDict.get('community', 'default')
						uniqname = personByUniqueNameDict.get('username', '')
						id = personByUniqueNameDict.get('id',-1)
						personByUniqueNameDict.update(_personDict)
						personByUniqueNameDict['community'] = community
						personByUniqueNameDict['username'] = uniqname
						personByUniqueNameDict['id'] = id
						return personByUniqueNameDict
			else:
				#this is the case where a person is identified in subsequent job actions. E.g., a secondary internal appointment
				personByUniqueNameDict = personSQL.getPersonByCommunityUserName(self.connection,_personDict)
				if personByUniqueNameDict:
					_personDict['id'] = personByUniqueNameDict.get('id',-1)
		return _personDict

	def resetPersonPointers(self,fromPerson,toPerson,_jobTaskDict,now,username):
		jaService = jobActionSvc.JobActionService(self.connection)
		jobAction = jaService.getJobAction(_jobTaskDict.get('job_action_id',-1))
		if jobAction:
			jaService.resetPersonPointers(jobAction,toPerson,now,username,doCommit=False)
			personSQL.removeOrphan(self.connection,fromPerson)

	def handleIdentifyCandidate(self, _jobActionDict, _jobTaskDict, _personDict, _container, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the Person table row.
			self.createOrUpdatePerson(_jobTaskDict, _personDict, doCommit=False, now=_now, username = _username)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				firstName = _personDict.get('first_name','')
				middleName = _personDict.get('middle_name','')
				lastName = _personDict.get('last_name','')
				suffix = _personDict.get('suffix','')
				fullName = stringUtils.constructFullName(firstName, lastName, middleName, suffix)
				logDict['verb'] = constants.kJobActionLogVerbIdentifyCandidate
				logDict['item'] = "".join([_personDict.get('username',''), fullName]).strip()
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username,_dashboardConfigKeyName="dashboardEvents", doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e
