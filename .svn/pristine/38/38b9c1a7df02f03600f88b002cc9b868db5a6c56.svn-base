# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape
import MPSCore.utilities.exceptionUtils as excUtils
import MPSAppt.core.constants as constants
import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.lookupTableService as lookupSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.trackService as trackSvc
import MPSAppt.services.terminationService as terminationSvc
import MPSAppt.services.titleService as titleSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.jobActionResolverService as resolver
import MPSAppt.services.personService as personSvc
import MPSAppt.services.jobActionResolverService as resolverSvc
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.emailService as emailSvc
import MPSAppt.services.completionService as completionSvc
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSCore.utilities.mpsMath as mpsMath

class AbstractCreateJobActionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def _impl(self, connection, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptCreateJobAction')

		#   PCN Code is required.
		#   Workflow Code is required.

		positionid = kwargs.get('positionid', '')
		workflowid = kwargs.get('workflowid', '')
		if not positionid or not workflowid:
			self.redirect("/appt")
			return
		positionDict = positionSvc.getPostionById(connection, positionid)
		if not positionDict:
			raise excUtils.MPSValidationException("Position not found")

		wfService = workflowSvc.WorkflowService(connection)
		workflowDict = wfService.getWorkflowById(workflowid)
		if not workflowDict:
			raise excUtils.MPSValidationException("Workflow not found")

		positionSvc.updatePrimaryOrSecondaryPostionType(connection,positionDict,workflowDict.get('job_action_type_id',-1))

		titleId = kwargs.get('titleid', '')
		if titleId:
			titleDict = lookupSvc.getEntityByKey(connection, 'wf_title', titleId, _key='id')
			if not titleDict:
				raise excUtils.MPSValidationException("Title not selected")
			titleCode = titleDict.get('code', '')
			positionDict['title_id'] = titleDict.get('id',0)
			if not wfService.titleValidForWorkflow(titleCode, workflowDict.get('code')):
				raise excUtils.MPSValidationException("Workflow not valid for Title")

		formData = tornado.escape.json_decode(self.request.body)
		start_date = ''
		if formData.has_key('start_date'):
			start_date = formData.get('start_date','')
			if start_date <> '':
				start_date = self.validateStartDate(start_date)

		personDict = {}
		if kwargs.get('personid',None):
			personDict = personSvc.PersonService(connection).getPerson(kwargs.get('personid',-1))
		community = self.getUserProfileCommunity()
		username = self.getUserProfileUsername()
		now = self.getEnvironment().formatUTCDate()
		params = {}
		params['workflowDict'] = workflowDict
		params['positionDict'] = positionDict
		params['personDict'] = personDict
		params['titleDict'] = {}
		params['community'] = community
		params['username'] = username
		params['proposed_start_date'] = start_date
		appointStatus = lookupSvc.getEntityByKey(connection,"wf_appointment_status",constants.kAppointStatusInProgress)
		if not appointStatus:
			raise excUtils.MPSValidationException("Appointment status not found")

		params['appointment_status'] = appointStatus
		params['now'] = now
		jaService = jobActionSvc.JobActionService(connection)
		jobActionId = jaService.createWorkflow(params)
		jobAction = jaService.getJobAction(jobActionId)
		if kwargs.get("overrideDepartmentalAccess",False):
			primarydepartmentId = kwargs.get('primaryapptdeptid','')
			jaService.overrideJobActionDepartmentalAccess(jobActionId,None,primarydepartmentId,True)

		workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
		initItemCodes = workflow.mainContainer.containerDict.get('config',{}).get('initItemCodes',[])
		actionInfo = jaService.initializeJobAction(workflow, personDict, initItemCodes, self.getProfile(), now, username, doCommit=True)
		if actionInfo:
			if actionInfo.get('grantCandidateAccess', False):
				self.grantCandidateAccess(personDict)

		if workflow.mainContainer.getConfigDict().get('emails'):
			emailService = emailSvc.EmailService(connection, jobAction, _jobTaskDict=None, _container=workflow.mainContainer, _profile=self.getProfile(), _username=username, _now=now)
			emailService.prepareAndSendDirectiveEmails()

		terminationTypeId = kwargs.get('terminationtypeid','')
		if terminationTypeId:
			terminationItemCode = workflow.mainContainer.containerDict.get('terminationItemCode','')
			jobTask = jaService.getOrCreateJobTask(jobAction,workflow.getContainer(terminationItemCode),now,username)
			completionSvc.CompletionService(connection).createCompletion(self.getTerminateCompletionDict(jobTask,terminationTypeId))

		responseDict = self.getPostResponseDict('New ' + workflowDict.get('descr',) + " created")
		responseDict['redirect'] = '/appt/jobaction/%s' % str(jobActionId)
		self.write(tornado.escape.json_encode(responseDict))

	def getTerminateCompletionDict(self,jobTask,terminationTypeId):
		completionDict = {}
		completionDict['job_task_id'] = jobTask.get('id','')
		completionDict['termination_type_id'] = terminationTypeId
		completionDict['effective_date'] = ''
		completionDict['scheduled_date'] = ''
		return completionDict

	def validateStartDate(self,start_date):
		jErrors = []
		result = ''
		try:
			parsed = dateUtils.flexibleDateMatch(start_date, self.getSiteYearMonthDayFormat())
			result = dateUtils.formatUTCDateOnly(parsed)
		except Exception, e:
			jErrors.append({'code':'start_date', 'field_value': '', 'message': "Invalid Start Date"})
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)
		return result

class TrackChangeJobActionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptCreateJobAction'])

		connection = self.getConnection()
		try:
			appointment = jobActionSvc.JobActionService(connection).getAppointment(kwargs.get('appointmentid',-1))
			resolver.JobActionResolverService(connection,self.getSitePreferences())._resolveAppointment(None,appointment)
			title = titleSvc.TitleService(connection).getTitle(appointment.get('title_id',0))
			department = positionSvc.getDepartment(connection,appointment.get('position_id',0))
			position = positionSvc.getPostionById(connection,appointment.get('position_id',0))
			person = personSvc.PersonService(connection).getPerson(appointment.get('person_id',0))
			person['full_name'] = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
			applicableTrackChanges = titleSvc.TitleService(connection).getTrackChangeMapForAppointment(appointment)
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['department'] = department
			context['title'] = title
			context['person'] = person
			context['positionid'] = position.get('id',-1)
			context['trackchanges'] = applicableTrackChanges
			self.render("trackchange.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

class ReappointJobActionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)


	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptCreateJobAction'])

		connection = self.getConnection()
		try:
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			self.render("reappoint.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

class CredentialingJobActionHandler(AbstractCreateJobActionHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)


	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptCreateJobAction'])

		appointmentId = kwargs.get('appointmentid','')
		personId = kwargs.get('personid','')
		if not personId or not appointmentId:
			self.redirect("/appt")

		connection = self.getConnection()
		try:
			person = personSvc.PersonService(connection).getPerson(personId)
			workflowList = workflowSvc.WorkflowService(connection).getWorkflowEntriesForJATypes([constants.kJobActionTypeCredential])
			if not workflowList:
				raise excUtils.MPSValidationException("No workflow found for this job action")
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['fullname'] = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
			context['personid'] = person.get('id',-1)
			context['workflowlist'] = workflowList
			context['appointment_id'] = appointmentId
			self.render("credential.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()
			
	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptCreateJobAction')
		connection = self.getConnection()
		try:
			workflowId = kwargs.get('workflowid','')
			appointmentId = kwargs.get('appointmentid','')
			personId = kwargs.get('personid','')

			if not appointmentId or not workflowId or not personId:
				self.redirect("/appt")
				return

			appointment = jobActionSvc.JobActionService(connection).getAppointment(appointmentId)
			position = positionSvc.getPostionById(connection,appointment.get('position_id',''))
			kwargs['positionid'] = position.get('id','')
			kwargs['personId'] = personId

			self._impl(connection,**kwargs)
		finally:
			self.closeConnection()

class EnrollmentJobActionHandler(AbstractCreateJobActionHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptCreateJobAction'])

		appointmentId = kwargs.get('appointmentid','')
		personId = kwargs.get('personid','')
		if not personId or not appointmentId:
			self.redirect("/appt")

		connection = self.getConnection()
		try:
			person = personSvc.PersonService(connection).getPerson(personId)
			workflowList = workflowSvc.WorkflowService(connection).getWorkflowEntriesForJATypes([constants.kJobActionTypeEnroll])
			if not workflowList:
				raise excUtils.MPSValidationException("No workflow found for this job action")
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['fullname'] = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
			context['personid'] = person.get('id',-1)
			context['workflowlist'] = workflowList
			context['appointment_id'] = appointmentId
			self.render("enrollment.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()
			
	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptCreateJobAction')
		connection = self.getConnection()
		try:
			workflowId = kwargs.get('workflowid','')
			appointmentId = kwargs.get('appointmentid','')
			personId = kwargs.get('personid','')

			if not appointmentId or not workflowId or not personId:
				self.redirect("/appt")
				return

			appointment = jobActionSvc.JobActionService(connection).getAppointment(appointmentId)
			position = positionSvc.getPostionById(connection,appointment.get('position_id',''))
			kwargs['positionid'] = position.get('id','')
			kwargs['personId'] = personId

			self._impl(connection,**kwargs)
		finally:
			self.closeConnection()


class TerminateJobActionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)


	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptCreateJobAction'])

		appointmentId = kwargs.get('appointmentid','')
		personId = kwargs.get('personid','')
		if not personId or not appointmentId:
			self.redirect("/appt")

		connection = self.getConnection()
		try:
			person = personSvc.PersonService(connection).getPerson(personId)
			workflowList = workflowSvc.WorkflowService(connection).getWorkflowEntriesForJATypes([constants.kJobActionTypeTerminate])
			if not workflowList:
				raise excUtils.MPSValidationException("No workflow found for this job action")
			workflow = workflowList[0]
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['termination_types'] = terminationSvc.TerminationService(connection).getTerminationTypes()
			context['terminationText'] = 'Reason'
			context['fullname'] = stringUtils.constructFullName(person.get('first_name',''),person.get('last_name',''),person.get('middle_name',''),person.get('suffix',''))
			context['personid'] = person.get('id',-1)
			context['workflow'] = workflow
			context['appointment_id'] = appointmentId
			self.render("terminate.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

class Terminator(AbstractCreateJobActionHandler):
	logger = logging.getLogger(__name__)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptCreateJobAction')
		connection = self.getConnection()
		try:
			terminationTypeId = kwargs.get('terminationtypeid','')
			workflowId = kwargs.get('workflowid','')
			appointmentId = kwargs.get('appointmentid','')
			personId = kwargs.get('personid','')

			if not appointmentId or not terminationTypeId or not workflowId or not personId:
				self.redirect("/appt")
				return

			appointment = jobActionSvc.JobActionService(connection).getAppointment(appointmentId)
			position = positionSvc.getPostionById(connection,appointment.get('position_id',''))
			kwargs['positionid'] = position.get('id','')
			kwargs['personId'] = personId
			kwargs['terminationtypeid'] = terminationTypeId

			self._impl(connection,**kwargs)
		finally:
			self.closeConnection()

class RecredentialJobActionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptCreateJobAction'])

		connection = self.getConnection()
		try:
			appointmentId = kwargs.get('appointmentid',-1)

			sitePreferences = self.getProfile().get('siteProfile',{}).get('sitePreferences',{})
			jobactionService = jobActionSvc.JobActionService(connection)

			appt = jobactionService.getAppointment(appointmentId)
			position = positionSvc.getPostionById(connection,appt.get('position_id',-1))
			primaryappt = resolverSvc.JobActionResolverService(connection,sitePreferences).appointmentResolveByPosition(appt,position)
			workflowList = workflowSvc.WorkflowService(connection).getWorkflowEntriesForMetatackAndJAType(primaryappt.get('metatrack',{}).get('id',-1),[constants.kJobActionTypeRecredential])
			person = primaryappt.get('person',{})

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['primary_appt'] = primaryappt
			context['person'] = person
			context['workflowlist'] = workflowList
			context['position_id'] = position.get('id',0)
			context['title_id'] = primaryappt.get('title',{}).get('id',0)
			context['person_id'] = person.get('id',-1)
			self.render("recredential.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()


class PromoteJobActionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptCreateJobAction'])

		connection = self.getConnection()
		try:
			personId = kwargs.get('personid',-1)
			appointmentId = kwargs.get('appointmentid',-1)
			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()

			sitePreferences = self.getProfile().get('siteProfile',{}).get('sitePreferences',{})
			person = personSvc.PersonService(connection).getPerson(personId)
			jobactionService = jobActionSvc.JobActionService(connection)
			appointments = jobactionService.getResolvedAppointmentsForPerson(person,sitePreferences)

			promotableTitles = []
			appointment = jobActionSvc.JobActionService(connection).getAppointment(appointmentId)
			if appointment:
				titleSVC = titleSvc.TitleService(connection)
				title = titleSVC.getTitle(appointment.get('title_id',0))
				if title:
					track = trackSvc.TrackService(connection).getTrackForTrackId(title.get('track_id',0))
					if track:
						promotableTitles = titleSVC.getTitlesForTrackAboveRankOrder(track,title)

			for each in appointments:
				try:
					self.validateUserHasAccessToJobAction(connection,community,username,each.get('jobAction',{}))
					each.get('appointment',{})['url'] = self.getJobActionUrl(each.get('jobAction',{}))
				except:
					each.get('appointment',{})['url'] = ''

			primaryappt = self.getPrimaryAppt(appointments)
			workflowList = workflowSvc.WorkflowService(connection).getWorkflowEntriesForMetatackAndJAType(primaryappt.get('metatrack',{}).get('id',-1),[constants.kJobActionTypePromotion])

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['primary_appt'] = primaryappt
			context['appointments'] = appointments
			context['person'] = appointments[0].get('person')
			context['workflowlist'] = workflowList
			context['position_id'] = appointment.get('position_id',0)
			context['person_id'] = person.get('id',-1)
			context['promotable_titles'] = promotableTitles
			context['is_promotable'] = self.getIsPromotable(appointments,promotableTitles)
			self.render("promotion.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

	def getIsPromotable(self,appointments,titles):
		if len(titles) == 0:
			return False
		for appointment in appointments:
			thisAppt = appointment.get('appointment',{})
			if thisAppt.get('apptstatus_code','') == 'INPROGRESS':
				jAction = appointment.get('jobAction',{})
				if jAction:
					if jAction.get('jobActionType',{}).get('code') == "PROMOTION":
						return False
		return True

	def getPrimaryAppt(self,appointments):
		for appt in appointments:
			if appt.get('appointment',{}).get('apptstatus_code','') == constants.kAppointStatusFilled:
				position = appt.get("position",{})
				if position.get('is_primary',False):
					return appt
		return {}

class CreateJobActionHandler(AbstractCreateJobActionHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		pass

	def post(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptCreateJobAction')
		connection = self.getConnection()
		try:
			self._impl(connection,**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)
		finally:
			if connection:
				self.closeConnection()


class EditJobActionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def post(self, **kwargs):
		try:
			self._getHandlerImpl('json', **kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyPermission('apptJobActionOverview')

		#   Job Action is required.
		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid or jobactionid == 'undefined':
			self.redirect("/appt/page/roster")
			return

		connection = self.getConnection()
		try:
			#   Must find Job Action.

			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			#   'json' mode returns the actual Job Action workflow data.

			self.jobActionId = jobactionid
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			if (mode == 'json'):
				self.set_header('Content-Type','application/json')
				workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())
				jaResolver = resolverSvc.JobActionResolverService(connection, self.getSitePreferences())
				appointment = jaResolver._resolveAppointment(None,jaService.getAppointment(jobAction.get('appointment_id')))
				canCancelJobAction = self.hasPermission('apptCancelJobAction')
				if jaService.appointmentIsInProgress(appointment):
					jobAction['cancel_url'] = '/appt/jobaction/cancel/%i' % (jobAction.get('id',-1))
				else:
					canCancelJobAction = False
					jobAction['cancel_url'] = ''

				jobAction['resendemail_url'] = '/appt/jobaction/resendemail/%i' % (jobAction.get('id',-1))
				jobAction['edit_start_date_url'] = '/appt/jobaction/editstartdate/%i' % (jobAction.get('id',-1))
				rawProposedStartDate = jobAction.get('proposed_start_date','')
				countDownClockPrefs = workflow.getMainContainer().getConfigDict().get('countdown_clock',{})
				countDownDays = jaService.calculateCountDownDays(rawProposedStartDate,countDownClockPrefs,self.getProfile())
				countDownDays,countDownWarning = self.getCountdownWarning(countDownClockPrefs,countDownDays,workflow,self.getProfile())

				jobAction['countdown_warning'] = countDownWarning
				jobAction['countdown_days'] = countDownDays
				jsonContext = jaResolver.resolve(jobAction)
				jsonContext['canCancelJobAction'] = canCancelJobAction
				jsonContext['leftNavWorkflows'] = self.getLeftNavList(jobAction,workflow)
				jsonContext['historicalIndicatorStatus'] = self.getHistoricalIndicator(appointment,jobAction)
				jsonContext['canResendEmail'] = self.hasPermission('apptResendEmail')
				jsonContext['workflow'] = workflow.getJobActionUI(self.getSitePreferences())
				if jobAction.get('cancelation_date','') <> '':
					self.appendCancelationToActivityLog(jobAction,jsonContext['workflow'])
				jsonContext['workflow']['data']['workflow'] = self._resolveWorkflow(connection, jobAction)
				jsonContext['show_proposed_start'] = workflow.mainContainer.containerDict.get('show_proposed_start_date',True)
				jsonContext['workflow']['data']['job_action_type'] = self._resolveJobActionType(connection, jsonContext['workflow']['data']['workflow'])
				jsonContext['status'] = workflow.computeStatus()
				jsonContext['auth'] = context.get('auth', {})
				jsonContext['date_format'] = dateUtils.mungeDatePatternForDisplay(self.getSiteYearMonthDayFormat())
				jsonContext['revisions_required_comment'] = self.getRevisionsRequiredComment(workflow)
				self.write(tornado.escape.json_encode(jsonContext))
				return

			#   'html' mode returns the page frame.
			context['bodyClass'] = 'FullView'
			if self.hasPermission('apptCandidate'):
				context['bodyClass'] = 'CandidateView'

			self.render("jobaction.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def getCountdownWarning(self,countdownClockPrefs,countDownDays,workflow,profile):
		warningDays = mpsMath.getIntFromString(profile.get('siteProfile',{}).get('sitePreferences',{}).get('defaultcountdownwarningdays','10'))
		if not countDownDays:
			return None,False
		if countDownDays <= warningDays:
			completionContainer = workflow.getContainer(countdownClockPrefs.get('completionContainer',''))
			if completionContainer and completionContainer.isComplete():
				#   in the case that the completion container is complete, don't show countdown days
				return None,False
			else:
				#   still in department's court
				return countDownDays,True
		return countDownDays,False

	def getLeftNavList(self, thisJobAction,thisWorkflow):
		# if a job action is selected that has related job action, the related job actions are listed sequentially
		# if there are other active job actions that are not related to the current job action,
		# those outliers will be listed in no particular order.
		displayedInNavIds = []
		jaSvc = jobActionSvc.JobActionService(self.getDbConnection())
		wfSvc = workflowSvc.WorkflowService(self.getDbConnection())
		navList = []
		jobActionsToShow = []
		thisJobAction['related_ja_id'] = thisJobAction.get('id',-1)
		jobActionsToShow.append(thisJobAction)
		displayedInNavIds.append(thisJobAction.get('id',-1))
		relatedJobActions = jaSvc.getRelatedJobActionDicts(thisJobAction.get('id',-1))
		for jobAction in relatedJobActions:
			jobAction['related_ja_id'] = thisJobAction.get('id',-1)
			jobActionsToShow.append(jobAction)
			displayedInNavIds.append(jobAction.get('id',-1))
		allJobActions = jaSvc.getCurrentJobActionsForPersonId(thisJobAction.get('person_id',-1))
		#	look for any other job action hanging out in outer space. This is probably an exceedingly rare case.
		for outlier in allJobActions:
			if not outlier.get('id',-1) in displayedInNavIds:
				jobActionsToShow.append(outlier)
				displayedInNavIds.append(outlier.get('id',-1))
		sortedList = sorted(jobActionsToShow, key=lambda k: k['id'])
		for ja in sortedList:
			if ja.get('id',0) == thisJobAction.get('id',-1):
				entry = self.getLeftNavEntry(ja,thisWorkflow,ja.get('id',-1),True)
			else:
				workflow = wfSvc.getWorkflowForJobAction(ja,self.getProfile())
				entry = self.getLeftNavEntry(ja,workflow,ja.get('id',-1),False)
			navList.append(entry)

		return navList

	def getLeftNavEntry(self,jobAction,workflow,relatedJAId,selected=False):
		status = workflow.computeStatus()
		numerator,denominator = workflow.getNumeratorAndDenominator()
		url = '/appt/jobaction/%i' % (jobAction.get('id',-1))
		try:
			self.validateUserHasAccessToJobAction(self.getDbConnection(), self.getUserProfileCommunity(), self.getUserProfileUsername(), jobAction)
		except:
			url = ''

		navEntry = {
				"title": workflow.mainContainer.containerDict.get('descr',''),
				"numerator": numerator,
				"denominator": denominator,
				"status_descr": status,
				"selected":selected,
				"related_ja_id":jobAction.get('related_ja_id',None),
				"workflow_url": url,
			}
		return navEntry

	def getRevisionsRequiredComment(self, workflow):
		returnVal = {}
		if workflow.jobActionDict.get('revisions_required',False):
			if workflow.activityLogCache:
				itemCode = workflow.activityLogCache[0].get('task_code','')
				revisions_required_comment_list = workflow.activityLogByTaskCodeCache.get(itemCode,[])
				if revisions_required_comment_list:
					commentDict = revisions_required_comment_list[0]
					returnVal = commentDict.copy()
					returnVal['comment'] = 'No comments recorded'
					returnVal['created'] = self.getUIDateTime(returnVal.get('created', ''))
					commentList = commentDict.get('comments',[])
					if commentList:
						comment = commentList[0]
						commentCode = comment.get('comment_code','')
						commentContainer = workflow.getContainer(itemCode)
						if commentContainer:
							commentConfig = commentContainer.getConfigDict().get('activityLog',{}).get('comments',[])
							for config in commentConfig:
								if commentCode == config.get('commentCode','z'):
									if self.hasAnyPermission(config.get('viewPermissions',[])):
										revisions_required_comment = commentDict.copy()
										revisions_required_comment['created'] = self.getUIDateTime(revisions_required_comment['created'])
										revisions_required_comment['comment'] = comment.get('comment','')
										return revisions_required_comment
		return returnVal

	def getUIDateTime(self,dateTimeString):
		localizedDate = self.localizeDate(dateTimeString)
		format = self.getSiteYearMonthDayHourMinuteFormat()
		formattedValue = dateUtils.parseDate(localizedDate,format)
		return formattedValue

	def getHistoricalIndicator(self,_appointment,jobAction):
		status = _appointment.get('apptstatus_code','')
		if status == 'ABANDONED':
			return constants.kAppointStatusAbandoned
		if status == 'FILLED':
			return constants.kAppointStatusFilled
		if status == 'HISTORICAL':
			return constants.kAppointStatusHistorical
		return ''

	def appendCancelationToActivityLog(self,_jobAction,_workflow):
		activityLogEntry = {}
		activityLogEntry['activity'] = 'Canceled'
		activityLogEntry['display_text'] = 'Canceled'
		comment = _jobAction.get('cancelation_comment','')
		activityLogEntry['comments'] = [{'comment':comment,'comment_code':'canceled'}]
		activityLogEntry['created'] = dateUtils.parseDate(_jobAction.get('cancelation_date',''),self.getSiteYearMonthDayFormat())
		activityLogEntry['task_code'] = 'canceled'
		activityLogEntry['username'] = _jobAction.get('cancelation_user','')
		_workflow.get('activity_log',[]).insert(0,activityLogEntry)


	def _resolveWorkflow(self, _dbConnection, _jobActionDict):
		workflowId = _jobActionDict.get('workflow_id', 0)
		if workflowId:
			workflowDict = lookupSvc.getEntityByKey(_dbConnection, 'wf_workflow', workflowId, _key='id')
			if workflowDict:
				return workflowDict

		return {}

	def _resolveJobActionType(self, _dbConnection, _workflowDict):
		jobActionTypeId = _workflowDict.get('job_action_type_id', 0)
		if jobActionTypeId:
			jobActionTypeDict = lookupSvc.getEntityByKey(_dbConnection, 'wf_job_action_type', jobActionTypeId, _key='id')
			if jobActionTypeDict:
				return jobActionTypeDict

		return {}


class CancelJobActionHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()

		#   Job Action is required.
		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		if not self.hasPermission('apptCancelJobAction'):
			self.redirect('/appt/jobaction/%s' % str(jobactionid))
			return

		connection = self.getConnection()

		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			resolvedJobAction = resolver.JobActionResolverService(connection,self.profile.get('siteProfile',{}).get('sitePreferences')).resolve(jobAction)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['job_action_id'] = jobactionid
			context['department_descr'] = resolvedJobAction.get('department',{}).get('descr')
			context['jobAction_descr'] = resolvedJobAction.get('job_action_type',{}).get('descr')
			context['pcn_descr'] = resolvedJobAction.get('position',{}).get('pcn')
			context['title_descr'] = resolvedJobAction.get('title',{}).get('descr','')

			self.render("cancelJobAction.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptCancelJobAction')

		#   Job Action is required.

		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			now = self.getEnvironment().formatUTCDate()
			appointment = jaService.getAppointment(jobAction.get('appointment_id'))
			formData = tornado.escape.json_decode(self.request.body)

			msg = 'Unable to cancel Job Action'
			if jaService.appointmentIsInProgress(appointment):
				try:
					result = completionSvc.CompletionService(connection).cancelJobAction(jobactionid, formData.get('comment', ''), now, username)
					if result:
						msg = 'Job Action Canceled'

				except Exception, e:
					if not (isinstance(e, excUtils.MPSException)):
						e = excUtils.wrapMPSException(e)
					self.logger.exception(e.getDetailMessage())

			responseDict = self.getPostResponseDict(msg)
			responseDict['redirect'] = '/appt'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

class ResendEmailHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()

		#   Job Action is required.
		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		if not self.hasPermission('apptResendEmail'):
			self.redirect('/appt/jobaction/%s' % str(jobactionid))
			return

		connection = self.getConnection()

		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			emailService = emailSvc.EmailService(connection,jobAction)
			emails = emailService.getEmailsForJobActionId()
			self.convertDatesForUI(emails)
			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			resolvedJobAction = resolver.JobActionResolverService(connection,self.profile.get('siteProfile',{}).get('sitePreferences')).resolve(jobAction)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['job_action_id'] = jobactionid
			context['department_descr'] = resolvedJobAction.get('department',{}).get('descr')
			context['jobAction_descr'] = resolvedJobAction.get('job_action_type',{}).get('descr')
			context['pcn_descr'] = resolvedJobAction.get('position',{}).get('pcn')
			context['title_descr'] = resolvedJobAction.get('title',{}).get('descr','')

			context['job_action_id'] = jobactionid
			context['emails'] = emails
			self.render("resendEmail.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()

	def convertDatesForUI(self,emails):
		for email in emails:
				datePref = self.getSiteYearMonthDayFormat()
				dateString = email.get('email_date','')
				if dateString:
					formattedValue = dateUtils.parseDate(dateString,datePref)
					email['email_date'] = formattedValue


	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyPermission('apptResendEmail')

		#   Job Action is required.

		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		emailid = kwargs.get('emailid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			now = self.getEnvironment().formatUTCDate()
			formData = tornado.escape.json_decode(self.request.body)
			selectedemailId = formData.get('selected_email','')
			recipient = formData.get('recipient_'+selectedemailId,'')

			msg = 'Unable to resend email'
			try:
				result = emailSvc.EmailService(connection,jobAction,_username=username,_now=now, _profile=self.getProfile()).resendEmail(selectedemailId,recipient)
				if result:
					msg = 'Email resent'

			except Exception, e:
				if not (isinstance(e, excUtils.MPSException)):
					e = excUtils.wrapMPSException(e)
				self.logger.exception(e.getDetailMessage())

			responseDict = self.getPostResponseDict(msg)
			responseDict['redirect'] = '/appt/jobaction/%i' % (jobAction.get('id',-1))
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()


class EditJobActionStartDateHandler(AbstractCreateJobActionHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def post(self, **kwargs):
		try:
			self._postHandlerImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()

		#   Job Action is required.

		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		connection = self.getConnection()
		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			#   User must have access to the Job Action's Department.

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			workflow = workflowSvc.WorkflowService(connection).getWorkflowForJobAction(jobAction, self.getProfile())

			formData = tornado.escape.json_decode(self.request.body)
			start_date = ''
			if formData.has_key('start_date'):
				start_date = formData.get('start_date','')
				if start_date <> '':
					start_date = self.validateStartDate(start_date)

			proposedStartChangeAlert = workflow.getMainContainer().containerDict.get('config',{}).get('proposed_start_date_change_alert',{})
			if proposedStartChangeAlert:
				self.sendStartDateChangeAlert(start_date,jobAction,proposedStartChangeAlert,workflow)

			msg = 'Start Date Saved'
			jaService.updateJobActionProposedStartDate(jobactionid, start_date)

			responseDict = self.getPostResponseDict(msg)
			responseDict['redirect'] = '/appt/jobaction/%i' % (jobAction.get('id',-1))
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def sendStartDateChangeAlert(self,newStartDate,_jobActionDict,proposedStartConfig,workflow):
		currentStartDate = _jobActionDict.get('proposed_start_date','')
		if currentStartDate == '':
			return
		if currentStartDate == newStartDate:
			return
		if self.getEmailOn(self.getProfile()):
			import MPSAppt.services.emailService as emailSvc
			currentStartDate = self.getDisplayDate(currentStartDate)
			newStartDate = self.getDisplayDate(newStartDate)
			now = self.getEnvironment().formatUTCDate()
			username = self.getUserProfileUsername()
			if workflow.mainContainer.getConfigDict().get('proposed_start_date_change_alert',{}).get('emailTextComplete',''):
				workflow.mainContainer.getConfigDict()['proposed_start_date_change_alert']['emailTextComplete'] = workflow.mainContainer.getConfigDict()['proposed_start_date_change_alert']['emailTextComplete'] % (currentStartDate,newStartDate)
			emailer = emailSvc.EmailService(self.dbConnection, _jobActionDict, {}, workflow.mainContainer, self.getProfile(), username, now, _alertConfigKeyName='proposed_start_date_change_alert')

			#   Alert emails.
			emailer.prepareAndSendAlertEmail(True)

	def getDisplayDate(self,_dateStr):
		displayDate = _dateStr
		try:
			localizedDate = dateUtils.localizeUTCDate(_dateStr,self.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('timezone','US/Eastern'))
			displayDate = dateUtils.parseDate(localizedDate,self.getProfile().get('siteProfile',{}).get('sitePreferences',{}).get('ymdformat','%m/%d/%Y'))
		except:
			pass
		finally:
			return displayDate

	def getEmailOn(self, _profile):
		if _profile:
			sitePreferences = _profile.get('siteProfile', {}).get('sitePreferences', {})
			if 'emailon' in sitePreferences:
				return stringUtils.interpretAsTrueFalse(sitePreferences['emailon'])

		return envUtils.getEnvironment().getEmailOn()


	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()

		#   Job Action is required.
		jobactionid = kwargs.get('jobactionid', '')
		if not jobactionid:
			self.redirect("/appt")
			return

		connection = self.getConnection()

		try:
			jaService = jobActionSvc.JobActionService(connection)
			jobAction = self.validateJobAction(jaService, jobactionid)

			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()
			self.validateUserHasAccessToJobAction(connection, community, username, jobAction)

			resolvedJobAction = resolver.JobActionResolverService(connection,self.profile.get('siteProfile',{}).get('sitePreferences')).resolve(jobAction)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['job_action_id'] = jobactionid
			context['start_date'] = resolvedJobAction.get('proposed_start_date','')
			context['department_descr'] = resolvedJobAction.get('department',{}).get('descr')
			context['jobAction_descr'] = resolvedJobAction.get('job_action_type',{}).get('descr')
			context['pcn_descr'] = resolvedJobAction.get('position',{}).get('pcn')
			context['title_descr'] = resolvedJobAction.get('title',{}).get('descr','')

			self.render("proposedStartDate.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
	(r"/appt/jobaction/create/(?P<positionid>[^/]*)/(?P<workflowid>[^/]*)/(?P<titleid>[^/]*)/(?P<personid>[^/]*)", CreateJobActionHandler),
	(r"/appt/jobaction/create/(?P<positionid>[^/]*)/(?P<workflowid>[^/]*)/(?P<titleid>[^/]*)", CreateJobActionHandler),
	(r"/appt/jobaction/create/(?P<pcn>[^/]*)/(?P<workflowcode>[^/]*)", CreateJobActionHandler),
	(r"/appt/jobaction/cancel/(?P<jobactionid>[^/]*)", CancelJobActionHandler),
	(r"/appt/jobaction/editstartdate/(?P<jobactionid>[^/]*)", EditJobActionStartDateHandler),
	(r"/appt/appointment/credential/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)", CredentialingJobActionHandler),
	(r"/appt/appointment/credential/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)/(?P<workflowid>[^/]*)", CredentialingJobActionHandler),
	(r"/appt/appointment/enroll/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)", EnrollmentJobActionHandler),
	(r"/appt/appointment/enroll/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)/(?P<workflowid>[^/]*)", EnrollmentJobActionHandler),
	(r"/appt/appointment/promote/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)", PromoteJobActionHandler),
	(r"/appt/appointment/recredential/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)", RecredentialJobActionHandler),
	(r"/appt/appointment/reappoint/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)", ReappointJobActionHandler),
	(r"/appt/appointment/terminate/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)", TerminateJobActionHandler),
	(r"/appt/appointment/terminate/(?P<appointmentid>[^/]*)/(?P<terminationtypeid>[^/]*)/(?P<workflowid>[^/]*)/(?P<personid>[^/]*)", Terminator),
	(r"/appt/appointment/trackchange/(?P<appointmentid>[^/]*)/(?P<personid>[^/]*)", TrackChangeJobActionHandler),
	(r"/appt/jobaction/resendemail/(?P<jobactionid>[^/]*)", ResendEmailHandler),
	(r"/appt/jobaction/(?P<jobactionid>[^/]*)", EditJobActionHandler),
]
