# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.jointPromotionsService as jointPromotionSvc
import MPSAppt.services.personService as personService
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.positionService as positionSvc

class JointPromotion(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setJointPromotions([])
		self.setShouldShow(True)
		self.loadInstance()
		if not self.getShouldShow():
			self.setIsEnabled(False)
	#   Getters/Setters.

	def getJointPromotions(self): return self.jointPromotionsList
	def setJointPromotions(self, _jointPromotionsList): self.jointPromotionsList = _jointPromotionsList

	def setShouldShow(self,_shouldShowValue): self.shouldShowValue = _shouldShowValue
	def getShouldShow(self): return self.shouldShowValue
	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return
		self.setIsLoaded(True)
		self.determineShowHide()
		if not self.getIsEnabled():
			return
		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultList = jointPromotionSvc.JointPromotionsService(self.getWorkflow().getConnection()).getJointPromotions(jobTask.get('id',-1))
			if resultList:
				self.setJointPromotions(resultList)

	def determineShowHide(self):
		# don't show if this promotion is a secondary
		position = positionSvc.getPostionById(self.getWorkflow().getConnection(), self.getWorkflow().jobActionDict.get('position_id',0))
		if position:
			if not position.get('is_primary'):
				self.setShouldShow(False)
				return
		# don't show if there are no secondaries
		person = personService.PersonService(self.getWorkflow().getConnection()).getPerson(self.getWorkflow().jobActionDict.get('person_id',0))
		if person:
			secondaryAppointments = jobActionSvc.JobActionService(self.getWorkflow().getConnection()).getResolvedSecondaryAppointmentsForPerson(person,{})
			if not secondaryAppointments:
				self.setShouldShow(False)
				return

	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			dataDict = {}
			dataDict['url'] = self._getURL()
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict
		return {}


	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEditContext(_sitePreferences)
			context['url'] = self._getURL()
			context['instructional'] = self.getConfigDict().get('instructional','')
			return context
		return {}

	def _getURL(self, _prefix='/appt/jointpromotion/jobaction'):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/%s/%s' % (_prefix, jobActionIdStr, self.getCode())

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			if self.getJointPromotions():
				return True
		return False
