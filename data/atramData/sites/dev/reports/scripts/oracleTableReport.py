# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from data.reporting.baseReport import BaseReport
import MPSAppt.services.departmentService as departmentSvc
import time

kTemplateName = 'oracleTableTemplate.html'

class OracleTableReport(BaseReport):
	def __init__(self, _parameters):
		BaseReport.__init__(self, _parameters)

	def run(self):
		connection = self.getConnection()
		try:
			oracleTableData = connection.executeSQLQuery('select * from oracle order by id',())
			self.emboldenOracleTableData(oracleTableData)
			if self.getExtension() == 'pdf':
				filePath = self.createPDF(oracleTableData)
			else:
				filePath = self.createTextFile(oracleTableData)
			self.persistReport(connection,filePath)
		finally:
			self.closeConnection()

	def emboldenOracleTableData(self,oracleTableData):
		i = 0
		for each in oracleTableData:
			oracleTableData[i]['data'] = oracleTableData[i]['data'].replace('Guido',' <b>Guido</b>')
			oracleTableData[i]['data'] = oracleTableData[i]['data'].replace('Gottasuiti',' <b>Gottasuiti</b>')
			oracleTableData[i]['data'] = oracleTableData[i]['data'].replace('Glidewalker',' <b>Glidewalker</b>')
			oracleTableData[i]['data'] = oracleTableData[i]['data'].replace('Smokey',' <b>Smokey</b>')
			oracleTableData[i]['data'] = oracleTableData[i]['data'].replace('Glidey',' <b>Glidey</b>')
			oracleTableData[i]['data'] = oracleTableData[i]['data'].replace('Bearette',' <b>Bearette</b>')
			i += 1


	def createPDF(self,oracleTableData):
		context = self.getInitialContext()
		context['oracleTableData'] = oracleTableData
		context['reportingcss'] = self.context.get('reportingcss','')
		uiPath,fullPath = self.generatePDF(self.getHTML(kTemplateName,context),"Oracle Table Report")
		return fullPath

	def createTextFile(self,oracleTableData):
		#create a list of lists and pass to generateCSV
		txtData = []
		txtData.append(self.getHeaders())
		for each in oracleTableData:
			row = []
			data = each.get('data')
			row.append(data)
			txtData.append(row)
		txtFilePath = self.generateTextFile(txtData)
		return txtFilePath

	def getHeaders(self):
		headers = []
		headers.append('Oracle Table Data')
		return headers

