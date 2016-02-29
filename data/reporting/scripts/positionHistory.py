# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from data.reporting.baseReport import BaseReport
import MPSAppt.services.departmentService as departmentSvc
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.jobActionService as jaService

kTemplateName = 'positionHistory.html'

class PositionHistory(BaseReport):
	def __init__(self, _parameters):
		BaseReport.__init__(self, _parameters)

	def run(self):
		connection = self.getConnection()
		try:
			departmentId = self.context.get('formData',{}).get('department',None)
			if not departmentId:
				return False
			department = departmentSvc.DepartmentService(self.connection).getDepartment(departmentId)

			if not department:
				return False

			context = self.getDepartmentHistoryContext(department)

			if self.getExtension() == 'pdf':
				filePath = self.createPDF(context)
			else:
				filePath = self.createTextFile(context)
			self.persistReport(connection,filePath)
		finally:
			self.closeConnection()

	def getDepartmentHistoryContext(self,department):
		context = self.getInitialContext()
		context['dept_descr'] =department.get('full_descr','')
		numpositions = 0
		actionsInProgress = 0
		departmentHistory = []
		positions = positionSvc.getPositionsForDepartment(self.connection,department)
		for position in positions:
			numpositions += 1
			sitePreferences = self.context.get('profile',{}).get('siteProfile',{}).get('sitePreferences',{})
			jaSvc = jaService.JobActionService(self.connection)
			appointments = jaSvc.getResolvedAppointmentsForPosition(position,sitePreferences)
			for each in appointments:
				jobAction = each.get('jobAction',{})
				if jobAction:
					if not jobAction.get('complete'):
						actionsInProgress += 1
						if not each.get('appointment',{}).get('start_date',''):
							if jobAction.get('proposed_start_date',''):
								each.get('appointment',{})['start_date'] = '*' + jobAction.get('proposed_start_date','')
					try:
						each.get('appointment',{})['url'] = self.getJobActionURL(each.get('jobAction', {}).get('id',-1))
					except:
						each.get('appointment',{})['url'] = ''
						pass
			positionDict = {'pcn':position.get('pcn'),"appointments":appointments,"numpositions":numpositions,"actionsInProgress":actionsInProgress}
			departmentHistory.append(positionDict)
		context['history']= departmentHistory
		context['numpositions'] = numpositions
		context['actionsInProgress'] = actionsInProgress
		return context

	def createPDF(self,context):
		context['reportingcss'] = self.context.get('reportingcss','')
		uiPath,fullPath = self.generatePDF(self.getHTML(kTemplateName,context),"Position History",_portrait=False)
		return fullPath

	def createTextFile(self,context):
		txtData = []
		txtData.append(self.getHeaders())
		for position in context.get('history',[]):
			pcn = position.get('pcn','')
			for appt in position.get('appointments',[]):
				fullname = appt.get('person').get('full_name','')
				track = appt.get('track').get('descr','')
				title = appt.get('title').get('descr','')
				jobActionType = ''
				jobAction = appt.get('jobAction')
				if jobAction:
					jobActionType = appt.get('jobAction').get('jobActionType',{}).get('descr','')
				status = appt.get('appointment').get('apptstatus_descr','')
				startDate = appt.get('appointment').get('start_date','')
				endDate = appt.get('appointment').get('end_date','')
				body = []
				body.append(pcn)
				body.append(fullname)
				body.append(track)
				body.append(title)
				body.append(jobActionType)
				body.append(status)
				body.append(startDate)
				body.append(endDate)
				txtData.append(body)
		txtFilePath = self.generateTextFile(txtData)
		return txtFilePath

	def getHeaders(self):
		headers = []
		headers.append('PCN')
		headers.append('Name')
		headers.append('Track')
		headers.append('Title')
		headers.append('Action')
		headers.append('Status')
		headers.append('Start Date')
		headers.append('End Date')
		return headers

