# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from data.reporting.baseReport import BaseReport
import MPSAppt.services.departmentService as departmentSvc
import time

kTemplateName = 'departmentListing.html'

class DepartmentListing(BaseReport):
	def __init__(self, _parameters):
		BaseReport.__init__(self, _parameters)

	def run(self):
		connection = self.getConnection()
		try:
			sortOrder = 'code'
			if self.context.get('formData',{}).get('orderBy','') == "Department Name":
				sortOrder = 'UPPER(descr)'
			departments = departmentSvc.DepartmentService(connection).getAllDepartments(False,sortOrder)
			if self.getExtension() == 'pdf':
				filePath = self.createPDF(departments)
			else:
				filePath = self.createTextFile(departments)
			self.persistReport(connection,filePath)
		finally:
			self.closeConnection()

	def createPDF(self,departments):
		context = {}
		context['departments'] = departments
		context['reportingcss'] = self.context.get('reportingcss','')
		uiPath,fullPath = self.generatePDF(self.getHTML(kTemplateName,context),"Department Listing")
		return fullPath

	def createTextFile(self,departments):
		#create a list of lists and pass to generateCSV
		txtData = []
		apptmaxaddresslines = self.getPrefAsInt('apptmaxaddresslines',5)
		apptmaxaddresssuffixlines = self.getPrefAsInt('apptmaxaddresssuffixlines',3)
		txtData.append(self.getHeaders(apptmaxaddresslines,apptmaxaddresssuffixlines))

		for department in departments:
			singleDepartmentDataList = []
			singleDepartmentDataList.append(department.get('code',''))
			singleDepartmentDataList.append(department.get('descr',''))

			address_lines = eval(department.get('address_lines'))
			counter = 0
			for line in address_lines:
				counter +=1
				singleDepartmentDataList.append(line)
			if counter < apptmaxaddresslines:
				while counter < apptmaxaddresslines:
					singleDepartmentDataList.append('')
					counter +=1
			singleDepartmentDataList.append(department.get('city',''))
			singleDepartmentDataList.append(department.get('state',''))
			singleDepartmentDataList.append(department.get('postal',''))

			suffixes = eval(department.get('address_suffix'))
			counter = 0
			for suffix in suffixes:
				counter +=1
				singleDepartmentDataList.append(suffix)
			if counter < apptmaxaddresslines:
				while counter < apptmaxaddresssuffixlines:
					singleDepartmentDataList.append('')
					counter +=1
			txtData.append(singleDepartmentDataList)

		txtFilePath = self.generateTextFile(txtData)
		return txtFilePath

	def getHeaders(self,apptmaxaddresslines,apptmaxaddresssuffixlines):
		headers = []
		headers.append('code')
		headers.append('description')
		i = 1
		while i <= apptmaxaddresslines:
			headers.append('address_line_%i' % (i))
			i += 1
		headers.append('city')
		headers.append('state')
		headers.append('zip')
		i = 1
		while i <= apptmaxaddresssuffixlines:
			headers.append('address_suffix_%i' % (i))
			i += 1
		return headers
	
