# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import pygal
from pygal import Config
from pygal.style import DefaultStyle

from data.reporting.baseReport import BaseReport
import MPSCore.utilities.dateUtilities as dateUtils
import MPSCore.utilities.stringUtilities as stringUtils
import MPSAppt.services.departmentService as departmentSvc

kTemplateName = 'timeToCompletion.html'

class TimeToCompletion(BaseReport):
	def __init__(self, _parameters):
		BaseReport.__init__(self, _parameters)

	def run(self):
		self.getConnection()
		try:
			timeToCompletionData = self.getRawTimeToCompletionJobActionData()
			jobActionAverages = self.computeJobActionAverages(timeToCompletionData)
			context = self.getInitialContext()
			context['jobActionAverages'] = jobActionAverages
			context['graph'] = self.renderJobActionAveragesGraph(jobActionAverages)
			if self.getExtension() == 'pdf':
				filePath = self.createPDF(context)
			else:
				filePath = self.createTextFile(context)
			self.persistReport(self.connection,filePath)
		finally:
			self.closeConnection()

	def createPDF(self,context):
		context['reportingcss'] = self.context.get('reportingcss','')
		context['start_date'] = self.context.get('formData',{}).get('startDate','')
		context['end_date'] = self.context.get('formData',{}).get('endDate','')
		uiPath,fullPath = self.generatePDF(self.getHTML(kTemplateName,context),"Time To Completion")
		return fullPath

	def createTextFile(self,context):
		txtData = []
		txtData.append(self.getHeaders())

		for jaType in context.get('jobActionAverages',[]):
			for item in jaType.get('items',[]):
				body = []
				body.append(item.get('job_action_type_descr',''))
				body.append(item.get('first_name',''))
				body.append(item.get('last_name',''))
				body.append(item.get('department_descr',''))
				body.append(item.get('title_descr',''))
				body.append(item.get('proposed_start_date',''))
				body.append(item.get('start',''))
				body.append(item.get('end',''))
				body.append(str(item.get('days','')))
				txtData.append(body)
		txtFilePath = self.generateTextFile(txtData)
		return txtFilePath

	def getHeaders(self):
		headers = []
		headers.append('Action')
		headers.append('First Name')
		headers.append('Last Name')
		headers.append('Department')
		headers.append('Title')
		headers.append('Proposed Start Date')
		headers.append('Date Action Started')
		headers.append('Date Action Completed')
		headers.append('Days')
		return headers

	def computeJobActionAverages(self,completedJobActions):
		departmentCache = departmentSvc.DepartmentService(self.connection).getDepartmentCacheWithFullDescr()

		jaTypeId = -1
		calculatedList = []
		currentJADict = {}
		for ja in completedJobActions:
			ja['url'] = self.getJobActionURL(ja.get('jobactionid', -1))
			if jaTypeId <> ja.get('ja_type_id',0):
				jaTypeId = ja.get('ja_type_id',0)
				departmentFullDescr = departmentCache.get(ja.get('department_code',{})).get('full_descr',ja.get('department_descr',''))
				currentJADict = {"jobActionTypeCode":ja.get('job_action_type_code',''),"jobActionType":ja.get('job_action_type_descr',''),"average":0,"items":[],"department_descr":departmentFullDescr,"title_descr":ja.get('title_descr','')}
				calculatedList.append(currentJADict)
				ja['department_descr'] = departmentFullDescr
			currentJADict['items'].append(ja)
		for each in calculatedList:
			each['average'],each['median'] = self.computeAverage(each)
		return calculatedList

	def computeAverage(self,segregatedType):
		itemCount = 0
		totalDays = 0
		daysArray = []
		for each in segregatedType.get('items',[]):
			itemCount += 1
			daysBetween = self.getDaysBetweenDateStrings(each.get('start',''),each.get('end',''))
			totalDays += daysBetween
			each['days'] = daysBetween
			each['startUTC'] = each['start']
			each['endUTC'] = each['end']
			each['start'] = self.formatDateForDisplay(each['start'])
			each['end'] = self.formatDateForDisplay(each['end'])
			each['proposed_start_date'] = self.formatDateForDisplay(each['proposed_start_date'])
			daysArray.append(daysBetween)
		if itemCount <> 0:
			return totalDays/itemCount,self.calculateMedianAverage(daysArray)
		return 0,0

	def calculateMedianAverage(self,integerArray):
		if not integerArray:
			return 0
		integerArray.sort()
		numIntegers = len(integerArray)
		if numIntegers % 2 == 0:
			#   even number of items - take middle two numbers of sorted list and calculate average
			return (integerArray[(numIntegers/2)] + integerArray[(numIntegers/2) - 1]) / 2
		else:
			#   odd number of items - return middle number of sorted list
			return integerArray[(numIntegers/2)]


	def getDaysBetweenDateStrings(self,startStr,endStr):
		startDate = dateUtils.parseUTCDate(startStr)
		endDate = dateUtils.parseUTCDate(endStr)
		delta = endDate - startDate
		return delta.days

	def getRawTimeToCompletionJobActionData(self):
		jobActions = self.getJobActions(self.context.get('formData',{}).get('startDate',None),
		                                self.context.get('formData',{}).get('endDate',None),
		                                self.context.get('formData',{}).get('department',''),
		                                self.context.get('formData',{}).get('title',''))
		return jobActions

	def renderJobActionAveragesGraph(self,jobActionAverages):
		if jobActionAverages:
			params = self.getGraphParams(jobActionAverages)
			aStyle = DefaultStyle(font_family='Arial',colors=self.getColors(),background='rgba(255,255,255,1)')
			config = Config()
			config.y_title = 'Days to Completion'
			config.x_title = 'Year'
			config.human_readable = True
			bar_chart2 = pygal.Bar(config,style=aStyle)
			bar_chart2.title = 'Time to Completion'
			bar_chart2.x_labels = map(str,params.get('dateRange',()))
			for item in params.get('items',[]):
				bar_chart2.add(item.get('title',''), item.get('days',[0]))

			return bar_chart2.render()
		return ''

	def getGraphParams(self,jobActionAverages):
		params = {}
		params['items'] = []
		config = self.context.get('config',{})
		start,end = self.getYearRange()
		if config.get('includeGraphs',False):
			for ja in jobActionAverages:
				if ja.get('jobActionTypeCode','') in config.get('graphingJobActionTypes',[]):
					items = ja.get('items',[])
					medianDaysList = self.calculateMedianAveragesByYear(items,start,end)
					params['items'].append({'title':ja.get('jobActionType',''),'days':medianDaysList})
			params['dateRange'] = range(start, end + 1)

		return params

	def calculateMedianAveragesByYear(self,items,start,end):
		totalsByYear = {}
		for i in range(start,end+1):
			totalsByYear[i] = []
		for item in items:
			year = self.getYear(item.get('startUTC',''))
			numDays = self.getDaysBetweenDateStrings(item.get('startUTC'),item.get('endUTC'))
			if totalsByYear.has_key(year):
				totalsByYear[year].append(numDays)
		medianByYear = []
		for i in range(start,end+1):
			medianByYear.append(self.calculateMedianAverage(totalsByYear[i]))
		return medianByYear

	def getYearRange(self):
		start,end = 0,0
		for control in self.context.get('reporting_params'):
			if control.get('controlName','') == 'startDate':
				start = control.get('input').year
			if control.get('controlName','') == 'endDate':
				end = control.get('input').year
		return start,end

	def getYear(self,dateStr):
		startDate = dateUtils.parseUTCDate(dateStr)
		return startDate.year

	def getJobActions(self,startDate,endDate,departments,titles):
		format = self.context.get('profile',{}).get('siteProfile',{}).get('sitePreferences',{}).get('ymdformat','')
		startDateStr = dateUtils.formatUTCDate(dateUtils.flexibleDateMatch(startDate, format))
		endDateStr = dateUtils.formatUTCDate(dateUtils.flexibleDateMatch(endDate, format))
		departmentList = stringUtils.getSQLInClause(departments,False)
		titleList = stringUtils.getSQLInClause(titles,False)

		sql = '''SELECT wf_job_action.id AS jobactionid,
		wf_department.descr AS department_descr,
		wf_department.code AS department_code,
		wf_job_action.job_action_type_id AS ja_type_id,
		wf_job_action_type.descr AS job_action_type_descr,
		wf_job_action_type.code AS job_action_type_code,
		wf_job_action.proposed_start_date AS proposed_start_date,
		wf_job_action.created AS start,
		wf_job_action.updated AS end,
		wf_title.descr AS title_descr,
		wf_title.code AS title_code,
		wf_person.first_name AS first_name,
		wf_person.last_name AS last_name
		FROM wf_job_action,wf_job_action_type,wf_position,wf_department,wf_person,wf_title
		WHERE job_action_type_id = wf_job_action_type.id AND
		wf_job_action.position_id = wf_position.id AND
		wf_job_action.person_id = wf_person.id AND
		wf_position.department_id IN''' + departmentList + ''' AND
		wf_position.title_id IN''' + titleList + ''' AND
		wf_department.id = wf_position.department_id AND
		wf_title.id = wf_position.title_id AND
		wf_job_action.complete = 't' AND
		wf_job_action.created BETWEEN %s AND %s AND
		wf_job_action.cancelation_date = ''
		ORDER BY wf_job_action.job_action_type_id,wf_title.code,wf_job_action.created '''
		args = (startDateStr,endDateStr,)
		return self.connection.executeSQLQuery(sql,args)