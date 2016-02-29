# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json

from MPSAppt.services.abstractResolverService import AbstractResolverService
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.lookupTableService as lookupSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.core.constants as constants
import MPSAppt.services.departmentResolverService as deptResolver

#   Given the following:
#       Job Action
#       database connection
#       site preferences
#
#   and optionally:
#       optional Appointment
#       optional Position
#       optional Person
#
#   this class returns a context containing the Job Action, plus its fully-resolved children,
#   with dates and timestamps converted to local (site) time, and formatted for UX display as per
#   the site preferences.

class JobActionResolverService(AbstractResolverService):
	def __init__(self, _connection, _sitePreferences):
		AbstractResolverService.__init__(self, _connection, _sitePreferences)
		self._initCaches()
		self.departmentResolver = deptResolver.DepartmentResolverService(_connection, _sitePreferences)

	def _initCaches(self):
		self.titleCache = {}
		self.trackCache = {}
		self.metaTrackCache = {}
		self.workflowCache = {}
		self.jobActionTypeCache = {}

		self.cachesLoaded = False

	def _loadCaches(self):
		if self.cachesLoaded:
			return

		self.cachesLoaded = True
		self.titleCache = lookupSvc.getLookupTable(self.connection, 'wf_title')
		self.trackCache = lookupSvc.getLookupTable(self.connection, 'wf_track')
		self.metaTrackCache = lookupSvc.getLookupTable(self.connection, 'wf_metatrack')
		self.workflowCache = lookupSvc.getLookupTable(self.connection, 'wf_workflow')
		self.jobActionTypeCache = lookupSvc.getLookupTable(self.connection, 'wf_job_action_type')


	#   Meat.

	def resolve(self, _jobActionDict, _optionalAppointmentDict=None, _optionalPositionDict=None, _optionalPersonDict=None):
		self._loadCaches()
		context = {}
		jobAction = _jobActionDict.copy()
		context['job_action'] = jobAction
		context['workflow'] = self._resolveWorkflow(context['job_action'])
		context['job_action_type'] = self._resolveJobActionType(context['workflow'])
		context['appointment'] = self._resolveAppointment(context['job_action'], _optionalAppointmentDict)
		context['position'] = self._resolvePosition(context['job_action'], _optionalPositionDict)
		context['title'] = self._resolveTitle(context['job_action'], context['appointment'], context['position'])
		context['track'] = self._resolveTrack(context['title'])
		context['metatrack'] = self._resolveMetatrack(context['track'])
		context['department'] = self._resolveDepartment(context['position'])
		context['person'] = self._resolvePerson(context['job_action'], _optionalPersonDict)

		self._resolveJobActionDates(jobAction)
		return context

	def appointmentResolveByPosition(self,appointmentDict,_positionDict):
		self._loadCaches()
		context = {}
		context['appointment'] = self._resolveAppointment(None,appointmentDict)
		context['department'] = {}
		context['position'] = {}
		if appointmentDict.get('position_id',None) <> None:
			position = positionSvc.getPostionById(self.connection,_positionDict.get('id',-1))
			context['position'] = self._resolvePosition(None,position)
			context['department'] = self._resolveDepartment(context['position'])
		jaSvc = jobActionSvc.JobActionService(self.connection)
		jobAction = jaSvc.getJobActionForApptId(appointmentDict.get('id',-1))
		if jobAction:
			jobAction['jobActionType'] = self.jobActionTypeCache.get(jobAction.get('job_action_type_id',None))
			jobAction['proposed_start_date'] = self.convertMDYToDisplayFormat(jobAction.get('proposed_start_date',''))
		context['jobAction'] = jobAction
		context['title'] = {}
		context['track'] = {}
		context['metatrack'] = {}
		if appointmentDict.get('title_id',None) <> None:
			title = lookupSvc.getEntityByKey(self.connection,'wf_title',appointmentDict.get('title_id'),'id')
			if title:
				context['title'] = title
			context['track'] = self._resolveTrack(context['title'])
			context['metatrack'] = self._resolveMetatrack(context['track'])
		context['person'] = self._resolvePerson(appointmentDict,None)
		return context

	def appointmentResolveByPerson(self,appointmentDict,_personDict):
		self._loadCaches()
		context = {}
		context['appointment'] = self._resolveAppointment(None,appointmentDict)
		context['department'] = {}
		context['position'] = {}
		if appointmentDict.get('position_id',None) <> None:
			position = positionSvc.getPostionById(self.connection,appointmentDict.get('position_id',-1))
			context['position'] = self._resolvePosition(None,position)
			context['department'] = self._resolveDepartment(context['position'])
		jaSvc = jobActionSvc.JobActionService(self.connection)
		jobAction = jaSvc.getJobActionForApptId(appointmentDict.get('id',-1))
		if jobAction:
			jobAction['jobActionType'] = self.jobActionTypeCache.get(jobAction.get('job_action_type_id',None))
		context['jobAction'] = jobAction
		context['title'] = {}
		context['track'] = {}
		context['metatrack'] = {}
		if appointmentDict.get('title_id',None) <> None:
			title = lookupSvc.getEntityByKey(self.connection,'wf_title',appointmentDict.get('title_id'),'id')
			if title:
				context['title'] = title
			context['track'] = self._resolveTrack(context['title'])
			context['metatrack'] = self._resolveMetatrack(context['track'])
		context['person'] = self._resolvePerson(None,_personDict)
		return context

	def _resolveAppointment(self, _jobAction, _optionalAppointmentDict):
		appointmentDict = {}
		if _optionalAppointmentDict is not None:
			appointmentDict = _optionalAppointmentDict
		else:
			appointmentId = _jobAction.get('appointment_id', 0)
			if appointmentId:
				appointmentDict = jobActionSvc.JobActionService(self.connection).getAppointment(appointmentId)

		if appointmentDict:
			appointmentDict['start_date'] = self.convertMDYToDisplayFormat(appointmentDict.get('start_date',''))
			appointmentDict['end_date'] = self.convertMDYToDisplayFormat(appointmentDict.get('end_date',''))
			appointmentDict['created'] = self.localizeAndConvertTimestampToDisplayFormat(appointmentDict.get('created',''))
			appointmentDict['updated'] = self.localizeAndConvertTimestampToDisplayFormat(appointmentDict.get('updated',''))
			appointmentDict['apptstatus_code'] = ''
			appointmentDict['apptstatus_descr'] = ''
			appointmentDict['person_url'] = ''
			if appointmentDict.get('person_id',None):
				appointmentDict['person_url'] = '/appt/person/%i' % (appointmentDict['person_id'])
			appointmentDict['position_url'] = ''
			if appointmentDict.get('position_id',None):
				appointmentDict['position_url'] = '/appt/pcn/%i' % (appointmentDict['position_id'])

			appointmentStatus = lookupSvc.getEntityByKey(self.connection,'wf_appointment_status',appointmentDict.get('appointment_status_id',-1),'id')
			if appointmentStatus:
				appointmentDict['apptstatus_code'] = appointmentStatus.get('code','')
				appointmentDict['apptstatus_descr'] = constants.kJobActionStatusDescriptionsDict.get(appointmentStatus.get('code',''),appointmentStatus.get('descr',''))

		return appointmentDict

	def _resolvePosition(self, _jobAction, _optionalPositionDict):
		positionDict = {}
		if _optionalPositionDict is not None:
			positionDict = _optionalPositionDict
			positionId = _optionalPositionDict.get('id', 0)
		else:
			positionId = _jobAction.get('position_id', 0)
			if positionId:
				positionDict = positionSvc.getPostionById(self.connection, positionId)

		if positionDict:
			positionDict['url'] = "/appt/pcn/%s" % str(positionId)
			positionDict['created'] = self.convertTimestampToDisplayFormat(positionDict.get('created',''))
			positionDict['updated'] = self.convertTimestampToDisplayFormat(positionDict.get('updated',''))

		return positionDict

	def _resolveTitle(self, _jobAction, _appointment, _position):
		titleId = _appointment.get('title_id', None)
		if not titleId:
			titleId = _position.get('title_id', None)
		if titleId:
			return self.titleCache.get(titleId, {})
		return {}

	def _resolveTrack(self, _title):
		trackId = _title.get('track_id', 0)
		if trackId:
			return self.trackCache.get(trackId, {})
		return {}

	def _resolveMetatrack(self, _track):
		metatrackId = _track.get('metatrack_id', 0)
		if metatrackId:
			return self.metaTrackCache.get(metatrackId, {})
		return {}

	def _resolveDepartment(self, _position):
		departmentId = _position.get('department_id', 0)
		if departmentId:
			return self.departmentResolver.resolve(departmentId)
		return {}

	def _resolvePerson(self, _jobAction, _optionalPersonDict):
		personDict = {}
		if _optionalPersonDict is not None:
			personDict = _optionalPersonDict
			personId = _optionalPersonDict.get('id',0)
		else:
			personId = _jobAction.get('person_id', 0)
			if personId:
				personDict = personSvc.PersonService(self.connection).getPerson(personId)

		if personDict:
			firstName = personDict.get('first_name', '')
			lastName = personDict.get('last_name', '')
			personDict['full_name'] = stringUtils.constructFullName(firstName, lastName, personDict.get('middle_name', ''), personDict.get('suffix', ''))
			personDict['last_comma_first'] = stringUtils.constructLastCommaFirstName(firstName, lastName)
			personDict['last_name_possessive'] = stringUtils.constructLastNamePossessive(lastName)
			personDict['url'] = "/appt/person/%s" % str(personId)
			personDict['created'] = self.convertTimestampToDisplayFormat(personDict.get('created',''))
			personDict['updated'] = self.convertTimestampToDisplayFormat(personDict.get('updated',''))

		return personDict

	def _resolveWorkflow(self, _jobAction):
		workflowId = _jobAction.get('workflow_id', 0)
		if workflowId:
			return self.workflowCache.get(workflowId, {})
		return {}

	def _resolveJobActionType(self, _workflow):
		jobActionTypeId = _workflow.get('job_action_type_id', 0)
		if jobActionTypeId:
			return self.jobActionTypeCache.get(jobActionTypeId, {})
		return {}

	def _resolveJobActionDates(self, _jobAction):
		_jobAction['created'] = self.convertTimestampToDisplayFormat(_jobAction.get('created',''))
		_jobAction['updated'] = self.convertTimestampToDisplayFormat(_jobAction.get('updated',''))
		_jobAction['completed'] = self.convertTimestampToDisplayFormat(_jobAction.get('completed',''))
		_jobAction['proposed_start_date'] = self.convertMDYToDisplayFormat(_jobAction.get('proposed_start_date',''))
