# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.services.titleService as titleSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.lookupTableService as lookupTableSvc
import MPSAppt.services.rosterEntryService as rosterEntrySvc
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.exceptionUtils as excUtils

class AbstractRosterEntryHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)


class RosterEntryHandler(AbstractRosterEntryHandler):
	logger = logging.getLogger(__name__)


	#   GET renders the Manual Roster Entry screen.

	def get(self, **kwargs):
		try:
			self._getHandlerImpl(**kwargs)
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self, **kwargs):
		self.verifyRequest()
		self.verifyAnyPermission(['apptRosterEntry'])

		connection = self.getConnection()
		try:

			#   Render the page.
			context = self.getInitialTemplateContext(self.getEnvironment())
			context['departments'] = deptSvc.DepartmentService(connection).getDepartmentHierarchy(None, _includeChairs=False)
			context['trackTitles'] = titleSvc.TitleService(connection).getTitlesByTrack()
			context['date_format'] = dateUtils.mungeDatePatternForDisplay(self.getSiteYearMonthDayFormat())

			context['community'] = 'default'
			communityList = self.getSiteCommunityList()
			if len(communityList) > 1:
				context['promptCommunity'] = True
				context['communityList'] = communityList

			self.render("rosterEntry.html", context=context, skin=context['skin'])

		finally:
			self.closeConnection()


	#   POST handles form submissions.

	def post(self, **kwargs):
		try:
			self._postImpl(**kwargs)
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postImpl(self, **kwargs):
		self.writePostResponseHeaders()
		self.verifyRequest()
		self.verifyAnyPermission(['apptRosterEntry'])

		connection = self.getConnection()
		try:
			#   Validate form data.

			formData = tornado.escape.json_decode(self.request.body)
			existingPersonDict = self.validateFormData(connection, formData)

			#   Construct dictionaries for the entities we need to create, then create.

			username = self.getUserProfileUsername()
			now = self.getEnvironment().formatUTCDate()

			personDict = self._getPersonDict(connection, formData, existingPersonDict, now, username)
			positionDict = self._getPositionDict(connection, formData, now, username)
			apptDict = self._getAppointmentDict(connection, formData, now, username)
			updateDemographics = formData.get('updateDemographics', True)
			rosterEntrySvc.RosterEntryService(connection).addRosterEntry(personDict, positionDict, apptDict, updateDemographics)

			responseDict = self.getPostResponseDict("Roster Item saved")
			responseDict['redirect'] = '/' + self.getEnvironment().getAppUriPrefix() + '/rosterEntry'
			self.write(tornado.escape.json_encode(responseDict))

		finally:
			self.closeConnection()

	def validateFormData(self, _connection, _formData):
		jErrors = []

		#   Check required fields.
		requiredFields = ['community','username','department_id','title_id','start_date']
		for fieldCode in requiredFields:
			fieldValue = _formData.get(fieldCode, '').strip()
			if not fieldValue:
				jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Username, if specified and already exists, can only have Secondary Appointments
		#   if the Username already has a Primary Appointment.
		personDict = None
		community = _formData.get('community', 'default')
		username = _formData.get('username', '').strip().lower()
		if username:
			_formData['username'] = username
			personDict = personSvc.PersonService(_connection).getPersonByCommunityUserName(community, username)
			if (personDict) and (_formData.get('is_primary', 'false') == 'true'):
				personId = personDict.get('id', 0)
				jaService = jobActionSvc.JobActionService(_connection)
				apptList = jaService.getAppointmentsForPerson(personId)
				if apptList:
					filledStatusId = self._getFilledStatusId(_connection)
					if filledStatusId:
						for apptDict in apptList:
							if apptDict.get('appointment_status_id', 0) == filledStatusId:
								positionDict = positionSvc.getPostionById(_connection, apptDict.get('position_id', 0))
								if positionDict:
									if positionDict.get('is_primary', True):
										jErrors.append({'code': 'username', 'field_value': username, 'message': "Username already has a Primary Appointment"})

		#   Must specify whether or not to update person demographics
		#   if the person already exists.
		_formData['updateDemographics'] = True
		if personDict:
			demoUpdate = _formData.get('demo_update', '')
			if demoUpdate != 'true':
				_formData['updateDemographics'] = False

		#   More check required fields, if we need demographics.
		if _formData['updateDemographics']:
			requiredFields = ['first_name','last_name']
			for fieldCode in requiredFields:
				fieldValue = _formData.get(fieldCode, '').strip()
				if not fieldValue:
					jErrors.append({ 'code': fieldCode, 'field_value': '', 'message': 'Required' })

		#   Department, if specified, must be valid.
		departmentId = _formData.get('department_id', 0)
		if departmentId:
			departmentDict = deptSvc.DepartmentService(_connection).getDepartment(departmentId)
			if not departmentDict:
				jErrors.append({ 'code': 'department_id', 'field_value': '', 'message': 'Invalid Department' })
				_formData['department_id'] = int(departmentId)

		#   Title, if specified, must be valid.
		titleId = _formData.get('title_id', 0)
		if titleId:
			titleDict = titleSvc.TitleService(_connection).getTitle(titleId)
			if not titleDict:
				jErrors.append({ 'code': 'title_id', 'field_value': '', 'message': 'Invalid Title' })
				_formData['title_id'] = int(titleId)

		#   Start Date, if specified, must be valid.
		startDate = _formData.get('start_date', '').strip()
		if startDate:
			try:
				parsed = dateUtils.flexibleDateMatch(startDate, self.getSiteYearMonthDayFormat())
				_formData['start_date'] = "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
			except Exception, e:
				jErrors.append({'code': 'start_date', 'field_value': startDate, 'message': "Invalid Start date"})

		#   End Date, if specified, must be valid.
		endDate = _formData.get('end_date', '').strip()
		if endDate:
			try:
				parsed = dateUtils.flexibleDateMatch(endDate, self.getSiteYearMonthDayFormat())
				_formData['end_date'] = "%s-%s-%s" % (str(parsed.year).rjust(4,'0'), str(parsed.month).rjust(2,'0'), str(parsed.day).rjust(2,'0'))
			except Exception, e:
				jErrors.append({'code': 'end_date', 'field_value': endDate, 'message': "Invalid End date"})

		#   Narc if errors.
		if jErrors:
			raise excUtils.MPSValidationException(jErrors)

		return personDict

	def _getFilledStatusId(self, _connection):
		filledStatusDict = lookupTableSvc.getEntityByKey(_connection, 'wf_appointment_status', 'FILLED', _key='code')
		if filledStatusDict:
			return filledStatusDict.get('id', 0)
		return 0

	def _getPersonDict(self, _connection, _formData, _existingPersonDict, _now, _lastuser):
		personDict = {}
		if _existingPersonDict:
			personDict['id'] = _existingPersonDict.get('id', 0)
		personDict['community'] = _formData.get('community', '')
		personDict['username'] = _formData.get('username', '')
		personDict['first_name'] = _formData.get('first_name', '')
		personDict['middle_name'] = _formData.get('middle_name', '')
		personDict['last_name'] = _formData.get('last_name', '')
		personDict['suffix'] = _formData.get('suffix', '')
		personDict['email'] = _formData.get('email', '')
		personDict['employee_nbr'] = _formData.get('employee_nbr', '')
		personDict['created'] = _now
		personDict['updated'] = _now
		personDict['lastuser'] = _lastuser
		return personDict

	def _getPositionDict(self, _connection, _formData, _now, _lastuser):
		positionDict = {}
		positionDict['department_id'] = _formData.get('department_id', 0)
		positionDict['title_id'] = _formData.get('title_id', 0)
		positionDict['is_primary'] = True if _formData.get('is_primary', 'false') == 'true' else False
		positionDict['created'] = _now
		positionDict['updated'] = _now
		positionDict['lastuser'] = _lastuser
		return positionDict

	def _getAppointmentDict(self, _connection, _formData, _now, _lastuser):
		apptDict = {}
		apptDict['title_id'] = _formData.get('title_id', 0)
		apptDict['start_date'] = _formData.get('start_date', '')
		apptDict['end_date'] = _formData.get('end_date', '')
		apptDict['appointment_status_id'] = self._getFilledStatusId(_connection)
		apptDict['created'] = _now
		apptDict['updated'] = _now
		apptDict['lastuser'] = _lastuser
		return apptDict


#   All URL mappings for this module.

urlMappings = [
	(r'/appt/rosterEntry', RosterEntryHandler),
]
