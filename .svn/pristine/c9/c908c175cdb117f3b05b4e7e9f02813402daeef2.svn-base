# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import pygal
from pygal import Config
from pygal.style import DefaultStyle

from data.reporting.baseReport import BaseReport
import MPSAppt.services.departmentService as departmentSvc
import MPSCore.utilities.stringUtilities as stringUtils

kTemplateName = 'actionsInProgress.html'

class ActionsInProgress(BaseReport):
	def __init__(self, _parameters):
		BaseReport.__init__(self, _parameters)

	def run(self):
		self.getConnection()
		try:
			rawactionsInProgressData = self.getRawActionsInProgressData(self.context.get('formData',{}).get('department',[]))
			actionsInProgressData = self.dictifyActionsInProgress(rawactionsInProgressData)
			context = self.getInitialContext()
			context["total_actions"] = len(rawactionsInProgressData)
			context['actionsInProgress'] = actionsInProgressData
			context['graphs'] = self.getGraphs(rawactionsInProgressData)
			if self.getExtension() == 'pdf':
				filePath = self.createPDF(context)
			else:
				filePath = self.createTextFile(context)
			self.persistReport(self.connection,filePath)
		finally:
			self.closeConnection()

	def dictifyActionsInProgress(self,rawactionsInProgressData):
		departmentCache = departmentSvc.DepartmentService(self.connection).getDepartmentCacheWithFullDescr()
		actionsByDepartmentList = []
		departmentDict = {}
		currentDepartmentCode = ''
		for each in rawactionsInProgressData:
			if currentDepartmentCode <> each.get('department_code',''):
				currentDepartmentCode = each.get('department_code','')
				if departmentDict:
					actionsByDepartmentList.append(departmentDict)
				departmentFullDescr = departmentCache.get(currentDepartmentCode,{}).get('full_descr',each.get('department_descr',''))
				departmentDict = {"department_code":currentDepartmentCode,"department_descr":departmentFullDescr,"actions":[]}
			each['start'] = self.formatDateForDisplay(each['start'])
			each['end'] = self.formatDateForDisplay(each['end'])
			each['proposed_start_date'] = self.formatDateForDisplay(each['proposed_start_date'])
			each['url'] = self.getJobActionURL(each.get('jobactionid', -1))
			each['first_name'] = '' if each['first_name'] is None else each['first_name']
			each['last_name'] = '' if each['last_name'] is None else each['last_name']
			departmentDict['actions'].append(each)
		if departmentDict:
			actionsByDepartmentList.append(departmentDict)
		return actionsByDepartmentList

	def getGraphs(self,actionsInProgressData):
		graphsList = []
		config = self.context.get('config',{})
		if config.get('includeGraphs',False):
			jaTypeDescr = ''
			for jaTypeCode in config.get('graphingJobActionTypes',''):
				statusDict = {}
				for actioninProgress in actionsInProgressData:
					if jaTypeCode == actioninProgress.get('job_action_type_code',''):
						jaTypeDescr = actioninProgress.get('job_action_type_descr','')
						if not statusDict.has_key(actioninProgress.get('status','')):
							statusDict[actioninProgress.get('status','')] = 1
						else:
							statusDict[actioninProgress.get('status','')] += 1
				if statusDict:
					graphingParams = self.getGraphingParameters(statusDict,jaTypeDescr)
					graphsList.append(self.renderGraph(graphingParams))
		return graphsList

	def getGraphingParameters(self,statuses,jaTypeDescr):
		params = {"title":"%s " % jaTypeDescr + " Statuses","items":[]}
		total = 0
		for key in statuses:
			total += statuses[key]
		if total > 0:
			for key in statuses:
				item = {}
				percentage = (float(statuses[key])/total) * 100
				item['descr'] = key + " (%i - %3.1f%s)" % (statuses[key],percentage,"%")
				item['value'] = round(percentage,1)
				params['items'].append(item)
		return params


	def renderGraph(self,graphingParams):
		config = Config()
		config.legend_at_bottom = True
		config.legend_at_bottom_columns = 2
		config.margin_bottom = 30
		aStyle = DefaultStyle(font_family='Arial',colors=self.getColors(),background='rgba(255,255,255,1)')
		pie_chart = pygal.Pie(config,style=aStyle)
		pie_chart.title = graphingParams.get('title','')
		for each in graphingParams.get('items',[]):
			descr = each.get('descr','')
			value = each.get('value',0.0)
			pie_chart.add(descr,value)
		return pie_chart.render()

	def createPDF(self,context):
		context['reportingcss'] = self.context.get('reportingcss','')
		uiPath,fullPath = self.generatePDF(self.getHTML(kTemplateName,context),"Time To Completion")
		return fullPath

	def createTextFile(self,context):
		txtData = []
		txtData.append(self.getHeaders())

		for actionByDept in context.get('actionsInProgress',[]):
			for action in actionByDept.get('actions',[]):
				body = []
				body.append(action.get('department_descr',''))
				body.append(action.get('job_action_type_descr',''))
				body.append(action.get('first_name',''))
				body.append(action.get('last_name',''))
				body.append(action.get('title_descr',''))
				body.append(action.get('proposed_start_date',''))
				body.append(action.get('start',''))
				body.append(str(action.get('status','')))
				txtData.append(body)
		txtFilePath = self.generateTextFile(txtData)
		return txtFilePath

	def getHeaders(self):
		headers = []
		headers.append('Department')
		headers.append('Action Type')
		headers.append('First Name')
		headers.append('Last Name')
		headers.append('Title')
		headers.append('Proposed Start Date')
		headers.append('Date Action Started')
		headers.append('Status')
		return headers


	def getRawActionsInProgressData(self,departments):
		departmentList = stringUtils.getSQLInClause(departments,False)
		sql = '''SELECT wf_job_action.id AS jobactionid,
		wf_department.descr AS department_descr,
		wf_department.code AS department_code,
		wf_job_action.job_action_type_id AS ja_type_id,
		wf_job_action_type.descr AS job_action_type_descr,
		wf_job_action_type.code AS job_action_type_code,
		wf_job_action.current_status AS status,
		wf_job_action.proposed_start_date AS proposed_start_date,
		wf_job_action.created AS start,
		wf_job_action.updated AS end,
		wf_title.descr AS title_descr,
		wf_title.code AS title_code,
		wf_person.first_name AS first_name,
		wf_person.last_name AS last_name,
		wf_person.id AS person_id
		FROM wf_job_action
		LEFT OUTER JOIN wf_person ON wf_person.id=wf_job_action.person_id
		JOIN wf_job_action_type ON job_action_type_id = wf_job_action_type.id
		JOIN wf_position ON wf_job_action.position_id = wf_position.id
		JOIN wf_department ON wf_position.department_id IN''' + departmentList + ''' AND wf_department.id = wf_position.department_id
		JOIN wf_appointment ON wf_job_action.appointment_id = wf_appointment.id
		JOIN wf_title ON wf_title.id = wf_appointment.title_id
		WHERE wf_job_action.complete = 'f' AND
		wf_job_action.cancelation_date = ''
		ORDER BY wf_department.code,wf_job_action.job_action_type_id,wf_job_action.created;'''
		args = ()
		return self.connection.executeSQLQuery(sql,args)