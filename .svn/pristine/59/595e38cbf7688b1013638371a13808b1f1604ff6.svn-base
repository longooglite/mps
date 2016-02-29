# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.jobActionService as jaService

class PersonHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self, **kwargs):
		try:
			self._getHandlerImpl('html', **kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, mode, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptPersonView'])

		connection = self.getConnection()
		try:
			personId = kwargs.get('person_id',-1)
			community = self.getUserProfileCommunity()
			username = self.getUserProfileUsername()

			sitePreferences = self.getProfile().get('siteProfile',{}).get('sitePreferences',{})
			person = personSvc.PersonService(connection).getPerson(personId)
			jobactionService = jaService.JobActionService(connection)
			appointments = jobactionService.getResolvedAppointmentsForPerson(person,sitePreferences)

			for each in appointments:
				if each.get('jobAction',{}):
					try:
						isBlacklisted = self.validateUserHasAccessToJobAction(connection,community,username,each.get('jobAction',{}))
						each.get('appointment',{})['url'] = self.getJobActionUrl(each.get('jobAction',{}))
						if isBlacklisted:
							each.get('appointment',{})['url'] = ''
							each.get('appointment',{})['allowableJobActions'] = []
					except:
						each.get('appointment',{})['url'] = ''
						each.get('appointment',{})['allowableJobActions'] = []

			primaryappt = jobactionService.getPrimaryAppt(appointments)
			workflowList = workflowSvc.WorkflowService(connection).getWorkflowEntriesForMetatackAndJAType(primaryappt.get('metatrack',{}).get('id',-1),['PROMOTION'])

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
			context['appointments'] = appointments
			context['person'] = appointments[0].get('person')
			context['workflowlist'] = workflowList
			context['primary_appt'] = primaryappt
			context['person_id'] = person.get('id',-1)
			self.render("person.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


#   All URL mappings for this module.

urlMappings = [
    (r"/appt/person/(?P<person_id>[^/]*)", PersonHandler),
]
