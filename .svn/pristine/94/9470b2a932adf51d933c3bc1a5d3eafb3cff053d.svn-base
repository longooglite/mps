# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.titleService as titleSvc
import MPSAppt.services.jointPromotionsService as jointPromotionsSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.core.constants as constants
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractJointPromotionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _impl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		if not jobactionid or not taskcode:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassJointPromotion)
			if not container.hasEditPermission() and not container.hasViewPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			#   Find or create the Job Task.

			now = self.getEnvironment().formatUTCDate()
			jobTask = jaService.getOrCreatePrimaryJobTask(jobAction, container, now, username)
			formData = tornado.escape.json_decode(self.request.body)
			titlePositionList = self.getTitlePositionCombos(formData)

			jointPromotionsSvc.JointPromotionsService(connection).handleSubmit(jobAction, jobTask, titlePositionList, container, self.getProfile(), now, username)

			responseDict = self.getPostResponseDict()
			responseDict['success'] = True
			responseDict['successMsg'] = container.containerDict.get('successMsg','')

			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


	def getTitlePositionCombos(self,formData):
		titlePositionCombos = []
		positionKeys = []
		for key in formData:
			elements = key.split('|')
			if len(elements) == 2:
				if elements[0] == 'position':
					positionKeys.append(elements[1])
		for positionKey in positionKeys:
			titleDictKey = 'title|%s' % (positionKey)
			selectedTitleKey = formData.get(titleDictKey,None)
			if selectedTitleKey:
				titlePositionCombos.append({"position":positionKey,"title":selectedTitleKey})
		return titlePositionCombos


class JointPromotionHandler(AbstractJointPromotionHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.
		#   Task Code is required.

		jobactionid = kwargs.get('jobactionid', '')
		taskcode = kwargs.get('taskcode', '')
		if not jobactionid or not taskcode:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:


			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   Must find Container of proper class.

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
			container = self.validateTaskCode(workflow, taskcode, constants.kContainerClassJointPromotion)
			if not container.hasEditPermission() and not container.hasViewPermission():
				raise excUtils.MPSValidationException("Operation not permitted")

			if workflow.isContainerBlocked(container):
				responseDict = self.getPostResponseDict('Operation not permitted')
				responseDict['redirect'] = "/appt/jobaction/%s" % str(jobactionid)
				self.write(tornado.escape.json_encode(responseDict))
				return

			#   User must have access to the Job Action's Department.

			container.loadInstance()
			currentJointPromotions = container.getJointPromotions()

			sitePreferences = self.getProfile().get('siteProfile',{}).get('sitePreferences',{})
			person = personSvc.PersonService(connection).getPerson(jobAction.get('person_id',0))
			currentSecondaryAppointments = jaService.getResolvedSecondaryAppointmentsForPerson(person,sitePreferences)
			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['jobactionid'] = jobactionid
			context['taskcode'] = taskcode
			context['secondarypositions'] = self.buildSecondaryPositionsList(connection,currentSecondaryAppointments,currentJointPromotions)
			context.update(container.getEditContext(self.getSitePreferences()))

			self.render("jointPromotionForm.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


	def buildSecondaryPositionsList(self,_dbConnection,currentSecondaryAppointments,selectedJointPromotions):
		secondaryList = []
		ts = titleSvc.TitleService(_dbConnection)
		for appt in currentSecondaryAppointments:
			position = appt.get('position',{})
			track = appt.get('track',{})
			title = appt.get('title',{})
			department = appt.get('department',{})
			if position and track and title and department:
				promotableTitles = ts.getTitlesForTrackAboveRankOrder(track,title)
				secondaryDict = {}
				secondaryDict["department"] = department.get('full_descr','')
				secondaryDict["titles"] = promotableTitles
				secondaryDict["pcn"] = position.get('pcn','')
				secondaryDict["positionid"] = position.get('id',0)
				positionSelected,selectedTitleId = self.getSecondarySelections(secondaryDict,selectedJointPromotions)
				secondaryDict["position_is_selected"] = positionSelected
				secondaryDict["selected_title_id"] = selectedTitleId
				secondaryList.append(secondaryDict)
		return secondaryList

	def getSecondarySelections(self,currentSecondary,selectedJointPromotions):
		for selectedPosition in selectedJointPromotions:
			if currentSecondary.get('positionid',0) == selectedPosition.get('position_id',-1):
				return True,selectedPosition.get('title_id',0)
		return False,''

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		kwargs['complete'] = True
		self._impl(**kwargs)




# #   All URL mappings for this module.

urlMappings = [
	(r"/appt/jointpromotion/jobaction/(?P<jobactionid>[^/]*)/(?P<taskcode>[^/]*)", JointPromotionHandler),

]
