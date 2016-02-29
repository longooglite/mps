# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import pygal
from pygal import Config
from pygal.style import DefaultStyle

from data.reporting.baseReport import BaseReport
import MPSAppt.services.reportingService as reportingSvc
import MPSCore.utilities.dateUtilities as dateUtils
import MPSAppt.services.workflowService as workflowSvc
import MPSAppt.services.lookupTableService as lookieHere

kTemplateName = 'evaluationsMetricsTemplate.html'

class EvaluationsMetrics(BaseReport):
	def __init__(self, _parameters):
		BaseReport.__init__(self, _parameters)

	def run(self):
		connection = self.getConnection()
		try:
			itemCodes = self.context.get('config',[]).get('itemCodes',[])
			startDate = self.getReportParameter('startDate')
			endDate = self.getReportParameter('endDate')

			context = self.getEvalDataContext(itemCodes,startDate,endDate)
			if self.getExtension() == 'pdf':
				filePath = self.createPDF(context)
			else:
				filePath = self.createTextFile(context)
			self.persistReport(connection,filePath)
		finally:
			self.closeConnection()

	def getEvalDataContext(self,itemCodes,startDate,endDate):
		context = self.getInitialContext()
		context["start"] = startDate.strftime("%m/%d/%Y")
		context["end"] = endDate.strftime("%m/%d/%Y")
		context['metrics'] = []
		metric = {}
		rawEvalData = reportingSvc.ReportingService(self.connection).getEvalItemData(itemCodes,startDate,endDate,'wf_evaluator')
		evaluatorTypeCache = lookieHere.getLookupTable(self.connection,'wf_evaluator_type')
		currTaskCode = ''
		for eval in rawEvalData:
			if currTaskCode <> eval.get('task_code',''):
				if metric:
					self.calculateMetrics(metric)
					context['metrics'].append(metric)
				currTaskCode = eval.get('task_code','')
				taskdescr = ''
				component = workflowSvc.WorkflowService(self.connection).getComponentByCode(currTaskCode)
				if component:
					taskdescr = component.get('descr','')
				metric = {"description":taskdescr,
				          "nbrEvals":0,
				          "nbrEvalsRequiringApproval":0,
				          "pctApproved":'0',
				          "pctRequiringApproval":'0',
				          "nbrApproved":0,
				          "nbrHasResponse":0,
				          "pctHasResponse":0,
				          "nbrNoResponse":0,
				          "pctNoResponse":0,
				          "nbrDeclined":0,
				          "pctDeclined":0,
				          "nbrDenied":0,
				          "pctDenied":0,
				          "counterContactToResponseDays":0,
				          "avgFromContactToSubmission":'0',
				          "counterSolicitationToApproval":0,
				          "avgFromSolicitationToApproval":'0',
				          "counterResponseToApproval":0,
				          "avgFromResponseToApproval":'0',
				          }
			emailedDate = self.getDate(eval.get('emailed_date',''))
			approvedDate = self.getDate(eval.get('approved_date',''))
			approved = eval.get('approved',False)
			declinedDate = self.getDate(eval.get('declined_date',''))
			declined = eval.get('declined',False)
			uploadedDate = self.getDate(eval.get('uploaded_date',''))
			uploaded = eval.get('uploaded',False)
			evaluatorTypeId = eval.get('evaluator_type_id',-1)

			# metrics gathering
			metric['nbrEvals'] += 1
			if evaluatorTypeCache.has_key(evaluatorTypeId):
				requiresApproval = evaluatorTypeCache.get(evaluatorTypeId,False).get('requires_approval',False)
				if requiresApproval:
					metric['nbrEvalsRequiringApproval'] += 1
					if approvedDate and approved:
						metric['nbrApproved'] += 1
						metric['counterSolicitationToApproval'] = self.daysBetween(emailedDate,approvedDate)
						metric['counterResponseToApproval'] = self.daysBetween(uploadedDate,approvedDate)
			if uploadedDate and uploaded:
				metric["nbrHasResponse"] += 1
				metric['counterContactToResponseDays'] += self.daysBetween(emailedDate,uploadedDate)
			elif not uploadedDate and not uploaded:
				metric["nbrNoResponse"] += 1
			if declinedDate and declined:
				metric["nbrDeclined"] += 1
				metric['counterContactToResponseDays'] += self.daysBetween(emailedDate,declinedDate)
			if approvedDate and not approved:
				metric["nbrDenied"] += 1
		if metric:
			self.calculateMetrics(metric)
			context['metrics'].append(metric)

		return context

	def calculateMetrics(self,metric):
		if metric['counterContactToResponseDays'] <> 0:
			metric['avgFromContactToSubmission'] = "{:10.1f}".format((metric['counterContactToResponseDays']/float(metric['nbrHasResponse'])))
		if metric['nbrEvalsRequiringApproval'] <> 0:
			metric['avgFromSolicitationToApproval'] = "{:10.1f}".format((metric['counterSolicitationToApproval']/float(metric['nbrEvalsRequiringApproval'])))
			metric['avgFromResponseToApproval'] = "{:10.1f}".format((metric['counterResponseToApproval']/float(metric['nbrEvalsRequiringApproval'])))
		if metric['nbrEvalsRequiringApproval'] <> 0:
			metric['pctApproved'] = "{:10.1f}".format(float(metric['nbrApproved'])/float(metric['nbrEvalsRequiringApproval'])*100)
		if metric['nbrEvals'] <> 0:
			metric['pctHasResponse'] = "{:10.1f}".format(float(metric['nbrHasResponse'])/float(metric['nbrEvals'])*100)
			metric['pctNoResponse'] = "{:10.1f}".format(float(metric['nbrNoResponse'])/float(metric['nbrEvals'])*100)
			metric['pctDeclined'] = "{:10.1f}".format(float(metric['nbrDeclined'])/float(metric['nbrEvals'])*100)
			metric['pctDenied'] = "{:10.1f}".format(float(metric['nbrDenied'])/float(metric['nbrEvals'])*100)
			metric['pctRequiringApproval'] = "{:10.1f}".format(float(metric['nbrEvalsRequiringApproval'])/float(metric['nbrEvals'])*100)
		metric['graph'] = self.renderMetricsGraph(metric)

	def renderMetricsGraph(self,metric):
		if metric:
			aStyle = DefaultStyle(font_family='Arial',colors=self.getColors(),background='rgba(255,255,255,1)')
			config = Config()
			config.y_title = ''
			config.truncate_legend = 50
			config.x_title = 'Percent'
			config.y_labels = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)

			config.human_readable = True
			bar_chart = pygal.HorizontalBar(config,style=aStyle)
			bar_chart.title = metric.get('description','')
			bar_chart.add('Responded %s' % (metric.get('pctHasResponse').strip()) + '%', float(metric.get('pctHasResponse')))
			bar_chart.add('No Response %s' % (metric.get('pctNoResponse').strip()) + '%', float(metric.get('pctNoResponse')))
			bar_chart.add('Approved %s' % (metric.get('pctApproved').strip()) + '%', float(metric.get('pctApproved')))
			bar_chart.add('Declined %s' % (metric.get('pctDeclined').strip()) + '%', float(metric.get('pctDeclined')))
			bar_chart.add('Denied %s' % (metric.get('pctDenied').strip()) + '%', float(metric.get('pctDenied')))
			return bar_chart.render()
		return ''

	def daysBetween(self,start,end):
		if end and start:
			delta = end - start
			return delta.days
		return 0

	def getDate(self,dateStr):
		if not dateStr:
			return None
		try:
			aDate = dateUtils.parseUTCDate(dateStr)
			return aDate
		except:
			pass
		return None


	def createPDF(self,context):
		uiPath,fullPath = self.generatePDF(self.getHTML(kTemplateName,context),"Evaluations Metrics")
		return fullPath

	def createTextFile(self,context):
		#create a list of lists and pass to generateCSV
		txtData = []
		txtData.append(self.getHeaders())
		for metric in context.get('metrics'):
			row = []
			row.append(metric.get("description").strip())
			row.append(str(metric.get("nbrEvals")).strip())
			row.append(str(metric.get("nbrHasResponse")).strip())
			row.append(str(metric.get("pctHasResponse")).strip())
			row.append(str(metric.get("nbrNoResponse")).strip())
			row.append(str(metric.get("pctNoResponse")).strip())
			row.append(str(metric.get("nbrDeclined")).strip())
			row.append(str(metric.get("pctDeclined")).strip())
			row.append(str(metric.get("nbrDenied")).strip())
			row.append(str(metric.get("pctDenied")).strip())
			row.append(str(metric.get("nbrEvalsRequiringApproval")).strip())
			row.append(str(metric.get("pctRequiringApproval")).strip())
			row.append(str(metric.get("nbrApproved")).strip())
			row.append(str(metric.get("pctApproved")).strip())
			row.append(str(metric.get("avgFromContactToSubmission")).strip())
			row.append(str(metric.get("avgFromSolicitationToApproval")).strip())
			row.append(str(metric.get("avgFromResponseToApproval")).strip())
			txtData.append(row)
		txtFilePath = self.generateTextFile(txtData)
		return txtFilePath

	def getHeaders(self):
		headers = []
		headers.append('Evaluation Description')
		headers.append('Total evaluations')
		headers.append('Number Responded')
		headers.append('Percentage Responded')
		headers.append('Number No response')
		headers.append('Perentage No response')
		headers.append('Number Declined')
		headers.append('Percentage Declined')
		headers.append('Number Denied')
		headers.append('Percentage Denied')
		headers.append('Number Requiring Approval')
		headers.append('Percentage Requiring Approval')
		headers.append('Number Approved')
		headers.append('Percentage Approved')
		headers.append('Average days from solicitation to evaluator response')
		headers.append('Average days from solicitation to approval')
		headers.append('Average days from evaluator response to approval')
		return headers

