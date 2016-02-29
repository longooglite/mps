# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.personService as personSvc
import MPSAppt.services.departmentService as deptSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.jobActionService as jobActionSvc


class RosterEntryService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def addRosterEntry(self, _personDict, _positionDict, _apptDict, _updateDempgraphics, doCommit = True):

		#   Assign the given _personDict to a newly-created _positionDict, and link them via _apptDict.
		#   The _personDict may represent a new or existing wf_person.
		#   A new position is always created using _positionDict.
		#   A new appointment is always create using _apptDict.

		try:
			persSoyvice = personSvc.PersonService(self.connection)
			deptSoyvice = deptSvc.DepartmentService(self.connection)
			jobActionSoyvice = jobActionSvc.JobActionService(self.connection)

			#   Create or update the Person.
			personId = _personDict.get('id', 0)
			if personId:
				if _updateDempgraphics:
					persSoyvice.updatePerson(_personDict, doCommit=False)
			else:
				persSoyvice.createPerson(_personDict, doCommit=False)
				personId = self.connection.getLastSequenceNbr('wf_person')

			#   Create the Position.
			departmentId = _positionDict.get('department_id', 0)
			departmentDict = deptSoyvice.getDepartment(departmentId)
			positionId = positionSvc.createPosition(self.connection, _positionDict, departmentDict, doCommit=False)

			#   Create the Appointment.
			_apptDict['person_id'] = personId
			_apptDict['position_id'] = positionId
			jobActionSoyvice.createAppointment(_apptDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e
