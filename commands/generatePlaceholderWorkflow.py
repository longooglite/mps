# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import optparse
import sys
import os
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

usage = "Script to generate placeholder workflow. Input = tab delimited file - see generatewf.xlsx/txt files in sandbox"

kWorkflowSrc = '''
{workflowcode} = {
	"code": "{workflowcode}",
	"descr": "{descr}",
	"header": "{descr}",
	"componentType": "Workflow",
	"affordanceType":"",
	"metaTrackCodes":["Faculty","Lecturer","Supplemental"],
	"jobActionType":"{jobactionType}",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "{status}",
	"className": "Container",
	"containers": [{containers}],
	"config": {},
}
'''

kColumnSrc = '''
{tabcode} = {
	"code": "{tabcode}",
	"descr": "{descr}",
	"header": "{descr}",
	"componentType": "Container",
	"affordanceType":"Tab",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "{status}",
	"className": "Container",
	"containers": [{containers}]
}'''

kSectionSrc = '''
{sectioncode} = {
	"code": "{sectioncode}",
	"descr": "{descr}",
	"header": "{descr}",
	"componentType": "Container",
	"affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "{status}",
	"className": "Container",
	"containers": [{containers}]
}'''

kItemSrc = '''
{itemcode} = {
	"code": "{itemcode}",
	"comment":"",
	"descr": "{descr}",
	"header": "{descr}",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "{status}",
	"successMsg":"{descr} Complete",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "{descr}",
		},
	},
}
'''
class Generator():
	def __init__(self, _options,):
		self.option = _options

	def run(self):
		fileContents = self.getFileContents(self.option.filename)
		parsedContent = self.getParsedContent(fileContents)
		if fileContents:
			self.generateWorkflow(parsedContent)

	def generateWorkflow(self,fileContents):
		rootPath = os.path.expanduser("~/Desktop/workflow/")
		os.makedirs(rootPath)
		self.writeWorkflowMain(rootPath,fileContents)
		self.writeWorkflow(rootPath,fileContents)

	def writeWorkflow(self,rootPath,fileContents):
		idx = 1
		for column in fileContents['workflow']['columns']:
			containersPath = rootPath + 'column%i' % (idx) + '/' + 'containers/'
			itemsPath = rootPath + 'column%i' % (idx) + '/' + 'items/'
			os.makedirs(containersPath)
			self.writeInit(rootPath + 'column%i' % (idx) + '/')
			self.writeInit(containersPath)
			os.makedirs(itemsPath)
			self.writeInit(itemsPath)
			columnSrc = kColumnSrc
			columnSrc = columnSrc.replace("{tabcode}",column['code'])
			columnSrc = columnSrc.replace("{descr}",column['descr'])
			columnSrc = columnSrc.replace("{status}",column['status'])
			sectionCodes = self.getSectionCodes(column)
			columnSrc = columnSrc.replace("{containers}",sectionCodes)
			self.writeSrc(containersPath,column['code'],columnSrc)
			for section in column['sections']:
				sectionSrc = kSectionSrc
				sectionSrc = sectionSrc.replace("{sectioncode}",section['code'])
				sectionSrc = sectionSrc.replace("{descr}",section['descr'])
				sectionSrc = sectionSrc.replace("{status}",section['status'])
				itemCodes = self.getItemCodes(section)
				sectionSrc = sectionSrc.replace("{containers}",itemCodes)
				self.writeSrc(containersPath,section['code'],sectionSrc)
				for item in section['items']:
					itemSrc = kItemSrc
					itemSrc = itemSrc.replace("{itemcode}",item['code'])
					itemSrc = itemSrc.replace("{descr}",item['descr'])
					itemSrc = itemSrc.replace("{status}",item['status'])
					self.writeSrc(itemsPath,item['code'],itemSrc)
			idx += 1

	def writeWorkflowMain(self,rootPath,fileContents):
		columnContainers = self.getColumnCodes(fileContents)
		workflowSrc = kWorkflowSrc
		workflowSrc = workflowSrc.replace("{containers}",columnContainers)
		workflowSrc = workflowSrc.replace("{jobactionType}",fileContents['workflow_type'])
		workflowSrc = workflowSrc.replace("{descr}",fileContents['workflow_descr'])
		workflowSrc = workflowSrc.replace("{status}",fileContents['workflow_status'])
		workflowSrc = workflowSrc.replace("{workflowcode}",fileContents['workflow_code'])
		self.writeInit(rootPath)
		self.writeSrc(rootPath,fileContents['workflow_code'],workflowSrc)

	def writeSrc(self,path,fileName,content):
		f = open(path + fileName + '.py','w')
		f.write(content)
		f.flush()
		f.close()

	def writeInit(self,path):
		f = open(path + '__init__.py','w')
		f.write('')
		f.flush()
		f.close()

	def getItemCodes(self,section):
		codes = []
		for item in section['items']:
			codes.append('"' + item['code'] + '"')
		return ','.join(codes)

	def getSectionCodes(self,column):
		codes = []
		for section in column['sections']:
			codes.append('"' + section['code'] + '"')
		return ','.join(codes)

	def getColumnCodes(self,fileContents):
		codes = []
		for column in fileContents['workflow']['columns']:
			codes.append('"' + column['code'] + '"')
		return ','.join(codes)

	def getParsedContent(self,fileContents):
		parsedContent = {'workflow_type':'APPT','workflow':{"columns":[]}}
		for content in fileContents:
			if content and not content.strip().startswith("#"):
				elements = content.split('\t')
				elementId = elements[0].lower().strip()
				descr = elements[1].strip()
				code = elements[2].strip()
				status = elements[3].strip()
				if elementId == 'workflow':
					parsedContent['workflow_type'] = elements[4].strip()
					parsedContent['workflow_code'] = code
					parsedContent['workflow_descr'] = descr
					parsedContent['workflow_status'] = status
				elif elementId == 'column':
					column = {"code":code,"descr":descr,"status":status,"sections":[]}
					parsedContent['workflow']['columns'].append(column)
				elif elementId == 'section':
					section = {"code":code,"descr":descr,"status":status,"items":[]}
					currentColumn = parsedContent['workflow']['columns'][len(parsedContent['workflow']['columns'])-1]
					currentColumn['sections'].append(section)
				elif elementId == 'item':
					currentColumn = parsedContent['workflow']['columns'][len(parsedContent['workflow']['columns'])-1]
					currentSection = currentColumn['sections'][len(currentColumn['sections'])-1]
					item = {"code":code,"descr":descr,"status":status}
					currentSection['items'].append(item)
		return parsedContent

	def getFileContents(self,filePath):
		if not os.path.exists(filePath):
			print "File does not exist"
			sys.exit(0)
		f = None
		try:
			f = open(filePath,'rU')
			contents = f.readlines()
			return contents
		except Exception,e:
			print e.message
		finally:
			if f:
				f.close()

class GeneratorInterface:
	DESCR = usage

	def __init__(self):
		self.options = None
		self.args = None

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-f', '--file', dest='filename', default='', help='tab delimited import file')
		return parser


	def run(self, options):
		self.options = options
		try:
			generator = Generator(options)
			generator.run()
		except Exception, e:
			print e.message

def main():
	try:
		generatorInterface = GeneratorInterface()
		parser = generatorInterface.get_parser()
		(options, args) = parser.parse_args()
		result = generatorInterface.run(options)
	except Exception,e:
		result = (-1,e.message)

if __name__ == '__main__':
	result = main()
