# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
cvLoad.py
'''

import sys
import os
import os.path
import csv
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import logging
import logging.config
import string
import optparse
import ntpath
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.stringUtilities as stringUtils
from MPSCV.core import constants
import MPSCore.core.constants

import cStringIO

kDelimiter = "\t"

kAffordanceTypeInsert = '''INSERT INTO cv_affordance_type (code,descr) VALUES (%s, %s);'''
kAffordanceTypeUpdate = '''UPDATE cv_affordance_type SET descr = %s WHERE code = %s;'''
kDisplayModeInsert = '''INSERT INTO cv_display_mode (code,descr) VALUES (%s, %s);'''
kDisplayModeUpdate = '''UPDATE cv_display_mode SET descr = %s WHERE code = %s;'''
kCategoryInsert = '''INSERT INTO cv_category (code,descr,seq,parent_code,exclude_from_cv_display,user_sortable,list_display_mode_id,detail_display_mode_id, display_options) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
kCategoryUpdate = '''UPDATE cv_category SET descr = %s,seq = %s,parent_code = %s,exclude_from_cv_display = %s,user_sortable = %s,list_display_mode_id=%s,detail_display_mode_id=%s,display_options = %s WHERE code = %s;'''
kSubCategoryGroupInsert = '''INSERT INTO cv_sub_category_group (code,descr,category_id,seq) VALUES (%s,%s,%s,%s);'''
kSubCategoryGroupUpdate = '''UPDATE cv_sub_category_group SET descr = %s, seq = %s, category_id = %s WHERE code = %s;'''
kSubCategoryInsert = '''INSERT INTO cv_sub_category (code,descr,sub_category_group_id,seq) VALUES (%s,%s,%s,%s);'''
kSubCategoryUpdate = '''UPDATE cv_sub_category SET sub_category_group_id = %s, descr = %s, seq = %s WHERE code = %s;'''
kFieldGroupInsert = '''INSERT INTO cv_field_group (code,descr,category_id,seq) VALUES (%s,%s,%s,%s);'''
kFieldGroupUpdate = '''UPDATE cv_field_group SET descr = %s, seq = %s, category_id = %s WHERE code = %s;'''
kFieldInsert = '''INSERT INTO cv_field (code,descr,alt_descr,required,seq,display_on_list_seq,list_display_options,list_sort_key_seq,affordance_type_id,text_length,text_height,static_lookup_code,date_format,field_group_id,display_on_pdf_seq) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
kFieldUpdate = '''UPDATE cv_field SET descr = %s,alt_descr = %s,required = %s,seq = %s,display_on_list_seq = %s,list_display_options=%s,list_sort_key_seq=%s,affordance_type_id = %s,text_length = %s,text_height = %s,static_lookup_code = %s,date_format = %s,display_on_pdf_seq = %s WHERE code = %s and field_group_id = %s;'''
kStaticLookupInsert = '''INSERT INTO cv_static_lookup (lookup_key,code,descr,alt_descr,seq) VALUES (%s, %s, %s, %s, %s);'''
kStaticLookupUpdate = '''UPDATE cv_static_lookup SET descr = %s,alt_descr = %s,seq = %s WHERE lookup_key = %s AND code = %s;'''

kSelectorGroupInsert = '''INSERT INTO cv_selector_group (code,descr) VALUES (%s,%s)'''
kSelectorGroupUpdate = '''UPDATE cv_selector_group SET descr = %s WHERE code = %s'''
kSelectorInsert = '''INSERT INTO cv_selector (cv_selector_group_id,code,descr,style,seq) VALUES (%s,%s,%s,%s,%s)'''
kSelectorUpdate = '''UPDATE cv_selector SET cv_selector_group_id = %s,descr = %s,style = %s,seq = %s WHERE code = %s'''


class CVLoad(object):

	def __init__(self, options=None, args=None):
		self.host = "localhost"
		self.port = 5432
		self.dbname = 'mpsdev'
		self.user = 'mps'
		self.password = 'mps'
		self.loadType = 'all'
		self.db = None
		self.messageList = []
		self.site = 'dev'

		if options:
			if options.host: self.host = options.host
			if options.port: self.port = int(options.port)
			if options.dbname: self.dbname = options.dbname
			if options.user: self.user = options.user
			if options.password: self.password = options.password
			if options.loadType: self.loadType = options.loadType
			if options.site: self.site = options.site
		self.site = self.site.replace('-','_')

	def shutdown(self):
		self.db.closeMpsConnection()

	def process(self):
		try:
			self.connectToDatabase()
			if self.loadType == 'all' or self.loadType == 'meta':
				self.updateAffordanceTypes()
				self.updateDisplayModes()
				self.updateCategories()
				self.updateSubCategoryGroups()
				self.updateSubCategories()
				self.updateFieldGroups()
				self.updateFields()
				self.updateSelectors()
			if self.loadType == 'all' or self.loadType == 'lookup':
				self.updateGenericStaticLookup(constants.kCountryLookupKey,'countries.txt')
				self.updateGenericStaticLookup(constants.kDegreesLookupKey,'degrees.txt')
				self.updateGenericStaticLookup(constants.kGrantRolesLookupKey,'grant_roles.txt')
				self.updateGenericStaticLookup(constants.kGrantStatusesLookupKey,'grant_statuses.txt')
				self.updateGenericStaticLookup(constants.kWorkExpLookupKey,'work_experience.txt')
				self.updateGenericStaticLookup(constants.kYesNoLookupKey,'yesno.txt')
				self.updateGenericStaticLookup(constants.kGenderLookupKey,'genders.txt')
				self.updateStateStaticLookup(constants.kStateLookupKey,'states.txt')
				self.updateGenericStaticLookup(constants.kDepartmentLookupKey,'departments.txt')
				self.updateLicenseStaticLookup(constants.kLicenseLookupKey,'licenses.txt')
				self.updateGenericStaticLookup(constants.kPatentsRoleLookupKey,'patents_role.txt')
				self.updateGenericStaticLookup(constants.kSeminarTypesLookupKey,'seminar_types.txt')
				self.updateGenericStaticLookup(constants.kPublicationStatusLookupKey,'publication_status.txt')
				self.updateGenericStaticLookup(constants.kRegionsLookupKey,'regions.txt')
				self.updateGenericStaticLookup(constants.kEthnicityLookupKey,'ethnicity.txt')
				self.updateGenericStaticLookup(constants.kLanguageLookupKey,'language.txt')
				self.updateGenericStaticLookup(constants.kProgramLookupKey,'program.txt')
				self.updateGenericStaticLookup(constants.kTeachingRoleLookupKey,'teachingrole.txt')
				self.updateGenericStaticLookup(constants.kMastersRoleLookupKey,'mastersrole.txt')
				self.updateGenericStaticLookup(constants.kRoleInCommitteeLookupKey,'roleincommittee.txt')
				self.updateGenericStaticLookup(constants.kTermLookupKey,'terms.txt')
				self.updateGenericStaticLookup(constants.kFacultyRankLookupKey,'faculty_rank.txt')
				self.updateGenericStaticLookup(constants.kHospitalAffiliationLookupKey,'hospital_affiliation.txt')
				self.updateGenericStaticLookup(constants.kCommitteeScopeLookupKey,'committee_scope.txt')
				self.updateGenericStaticLookup(constants.kParticipationLookupKey,'participation.txt')
				self.updateGenericStaticLookup(constants.kAbstractTypeLookupKey,'abstract_type.txt')
				self.updateGenericStaticLookup(constants.kDissertationTypeLookupKey,'dissertation_type.txt')

				self.updateHelpText()
		except Exception, e:
			print e.message
			sys.exit(999)


	#UI Meta Data

	def updateFields(self):
		rawData = self.getImportFile('fields.txt')
		seq = 0
		for rawRow in rawData:
			if self.validRow(rawRow):
				seq += 1
				self.upsertField(rawRow,seq)

	def upsertField(self, fieldData,seq):
		field_group_id = self.getEntityIdByCode("cv_field_group",fieldData[0].strip())
		code = fieldData[1].strip()
		descr = fieldData[2].strip()
		alt_descr = fieldData[3].strip()
		required = self.getBool(fieldData[4])
		data_type_id = self.getEntityIdByCode("cv_affordance_type",fieldData[5].strip())
		seq = self.getInt(fieldData[6])
		display_on_pdf_seq = fieldData[7].strip()
		display_on_list_seq = fieldData[8].strip()
		list_display_options = fieldData[9].strip()
		list_sort_key_seq = self.getInt(fieldData[10])
		length = self.getInt(fieldData[11])
		height = self.getInt(fieldData[12])
		static_key = fieldData[13].strip()
		date_format = fieldData[14].strip()

		if self.db.getRowCount('cv_field', "code = '%s'" % (fieldData[1].strip())):
			args = (descr,alt_descr,required,seq,display_on_list_seq,list_display_options,list_sort_key_seq,data_type_id,length,height,static_key,date_format,display_on_pdf_seq,code,field_group_id)
			self.db.executeSQLCommand(kFieldUpdate,args)
		else:
			args = (code,descr,alt_descr,required,seq,display_on_list_seq,list_display_options,list_sort_key_seq,data_type_id,length,height,static_key,date_format,field_group_id,display_on_pdf_seq)
			self.db.executeSQLCommand(kFieldInsert,args)

	def getInt(self,str):
		stripped = str.strip()
		returnVal = 0
		try:
			returnVal = int(stripped)
		except Exception,e:
			pass
		return returnVal

	def updateSelectors(self):
		rawData = self.getImportFile("selector_groups.txt")
		if rawData:
			for rawRow in rawData:
				if self.validRow(rawRow):
					code = rawRow[0].strip()
					descr = rawRow[1].strip()
					if self.db.getRowCount('cv_selector_group', "code = '%s'" % (code)):
						args = (descr,code,)
						self.db.executeSQLCommand(kSelectorGroupUpdate,args)
					else:
						args = (code,descr,)
						self.db.executeSQLCommand(kSelectorGroupInsert,args)
		rawData = self.getImportFile("selectors.txt")
		if rawData:
			for rawRow in rawData:
				if self.validRow(rawRow):
					groupcode = rawRow[0].strip()
					code = rawRow[1].strip()
					descr = rawRow[2].strip()
					style = rawRow[3].strip()
					seq = self.getInt(rawRow[4])
					group_id = self.getEntityIdByCode("cv_selector_group",groupcode)
					if self.db.getRowCount('cv_selector', "code = '%s'" % (code)):
						args = (group_id,descr,style,seq,code,)
						self.db.executeSQLCommand(kSelectorUpdate,args)
					else:
						args = (group_id,code,descr,style,seq,)
						self.db.executeSQLCommand(kSelectorInsert,args)


	def updateCategories(self):
		rawData = self.getImportFile('categories.txt')
		seq = 0
		for rawRow in rawData:
			if self.validRow(rawRow):
				seq += 1
				self.upsertCategory(rawRow,seq)

	def upsertCategory(self, categoryData, seq):
		code = categoryData[0].strip()
		description = categoryData[1].strip()
		parent_code = categoryData[2].strip()
		exclude_from_cv_display = categoryData[3].strip()
		user_sortable = categoryData[4].strip()
		list_display_mode_id = self.getEntityIdByCode("cv_display_mode",categoryData[5].strip())
		detail_display_mode_id = self.getEntityIdByCode("cv_display_mode",categoryData[6].strip())
		display_options = categoryData[7]

		if self.db.getRowCount('cv_category', "code = '%s'" % (code)):
			self.db.executeSQLCommand(kCategoryUpdate,(description,
			                                                seq,
															parent_code,
			                                                exclude_from_cv_display,
			                                                user_sortable,
			                                                list_display_mode_id,
			                                                detail_display_mode_id,
			                                                display_options,
			                                                code))

		else:
			self.db.executeSQLCommand(kCategoryInsert,(code,
			                                                description,
															seq,
			                                                parent_code,
															exclude_from_cv_display,
															user_sortable,
			                                                list_display_mode_id,
			                                                detail_display_mode_id,
															display_options))

	def updateSubCategoryGroups(self):
		rawData = self.getImportFile('subcategoryGroups.txt')
		seq = 0
		for rawRow in rawData:
			if self.validRow(rawRow):
				seq += 1
				self.upsertSubCategoryGroups(rawRow, seq)

	def upsertSubCategoryGroups(self, subcategoryGroupData, seq):
		category_id = self.getEntityIdByCode("cv_category",subcategoryGroupData[0])
		subcategoryGroupCode = subcategoryGroupData[1].strip()
		subcategoryGroupDescr = subcategoryGroupData[2].strip()

		if self.db.getRowCount('cv_sub_category_group', "code = '%s'" % (subcategoryGroupCode)):
			self.db.executeSQLCommand(kSubCategoryGroupUpdate,(subcategoryGroupDescr,seq,category_id,subcategoryGroupCode))
		else:
			self.db.executeSQLCommand(kSubCategoryGroupInsert,(subcategoryGroupCode,subcategoryGroupDescr,category_id,seq))

	def updateSubCategories(self):
		rawData = self.getImportFile('subcategories.txt')
		seq = 0
		for rawRow in rawData:
			if self.validRow(rawRow):
				seq += 1
				self.upsertSubCategory(rawRow, seq)


	def upsertSubCategory(self, subcategoryData, seq):
		subCategoryGroupCode = subcategoryData[0].strip()
		subcategoryCode = subcategoryData[1].strip()
		subcategoryDescr = subcategoryData[2].strip()
		sub_category_group_id = self.getEntityIdByCode("cv_sub_category_group",subCategoryGroupCode)

		if self.db.getRowCount('cv_sub_category', "code = '%s'" % (subcategoryCode)):
			self.db.executeSQLCommand(kSubCategoryUpdate,(sub_category_group_id,subcategoryDescr,seq,subcategoryCode))
		else:
			self.db.executeSQLCommand(kSubCategoryInsert,(subcategoryCode,subcategoryDescr,sub_category_group_id,seq))

	def updateFieldGroups(self):
		rawData = self.getImportFile('fieldGroups.txt')
		seq = 0
		for rawRow in rawData:
			if self.validRow(rawRow):
				seq += 1
				self.upsertFieldGroups(rawRow, seq)

	def upsertFieldGroups(self, fieldGroupData, seq):
		category_id = self.getEntityIdByCode("cv_category",fieldGroupData[0])
		fieldGroupCode = fieldGroupData[1].strip()
		fieldGroupDescr = fieldGroupData[2].strip()

		if self.db.getRowCount('cv_field_group', "code = '%s'" % (fieldGroupCode)):
			self.db.executeSQLCommand(kFieldGroupUpdate,(fieldGroupDescr,seq,category_id,fieldGroupCode))
		else:
			self.db.executeSQLCommand(kFieldGroupInsert,(fieldGroupCode,fieldGroupDescr,category_id,seq))

	def getEntityIdByCode(self,entityName,code):
		sqlStr = "SELECT id FROM %s " % (entityName)
		sqlStr += "WHERE code = %s;"
		args = (code,)
		qry = self.db.executeSQLQuery(sqlStr,args)
		if len(qry) == 0:
			print "%s for %s was not found" % (code,entityName)
		return qry[0]['id']

	def updateAffordanceTypes(self):
		rawData = self.getImportFile('affordanceTypes.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertAffordanceTypes(rawRow)

	def upsertAffordanceTypes(self, affordanceData):
		if self.db.getRowCount('cv_affordance_type', "code = '%s'" % (affordanceData[0].strip())):
			self.db.executeSQLCommand(kAffordanceTypeUpdate,(affordanceData[1].strip(),
			                                       affordanceData[0].strip()))
		else:
			self.db.executeSQLCommand(kAffordanceTypeInsert,(affordanceData[0].strip(),
			                                             affordanceData[1].strip()))


	def updateDisplayModes(self):
		rawData = self.getImportFile('displayModes.txt')
		for rawRow in rawData:
			if self.validRow(rawRow):
				self.upsertDisplayModes(rawRow)

	def upsertDisplayModes(self, displayModeData):
		if self.db.getRowCount('cv_display_mode', "code = '%s'" % (displayModeData[0].strip())):
			self.db.executeSQLCommand(kDisplayModeUpdate,(displayModeData[1].strip(),
			                                            displayModeData[0].strip()))
		else:
			self.db.executeSQLCommand(kDisplayModeInsert,(displayModeData[0].strip(),
			                                             displayModeData[1].strip()))

	#static lookup data
	def updateGenericStaticLookup(self,lookupKey,fileName):
		rawData = self.getImportFile(fileName)
		i = 0
		for rawRow in rawData:
			if self.validRow(rawRow):
				i += 1
				items = rawRow
				code = self.getCode(items[0])
				descr = items[0].strip()
				alt_descr = ''
				nbrCols = len(rawRow)
				if nbrCols > 1:
					descr = items[1].strip()
					if nbrCols > 2:
						alt_descr = items[2].strip()
				self.upsertStaticLookup(lookupKey,code,descr,alt_descr,i)

	def updateLicenseStaticLookup(self,lookupKey,fileName,isCanned = True):
		rawData = self.getImportFile(fileName)
		i = 0
		for rawRow in rawData:
			if self.validRow(rawRow):
				i += 1
				items = rawRow
				code = self.getCode(items[0])
				altDescr = 'Medical License ' + items[0]
				self.upsertStaticLookup(lookupKey,code,items[0].strip(),altDescr,i)

	def updateStateStaticLookup(self,lookupKey,fileName):
		rawData = self.getImportFile(fileName)
		i = 0
		for rawRow in rawData:
			if self.validRow(rawRow):
				i += 1
				items = rawRow
				code,state = self.getCodeAndState(items[0])
				altDescr = 'State of ' + state
				self.upsertStaticLookup(lookupKey,code,items[0].strip(),altDescr,i)

	def getCodeAndState(self,val):
		splits = val.split("(")
		return splits[1].strip()[0:2],splits[0].strip()

	def upsertStaticLookup(self,lookupKey,code,descr,alt_descr,seq):
		whereClause = "lookup_key = '%s' AND code = '%s'" % (lookupKey,code)
		if self.db.getRowCount('cv_static_lookup', whereClause):
			self.db.executeSQLCommand(kStaticLookupUpdate,(descr,
			                                                alt_descr,
															seq,
															lookupKey,
															code))
		else:
			self.db.executeSQLCommand(kStaticLookupInsert,(lookupKey,
			                                               code,
			                                                descr,
			                                                alt_descr,
															seq))


	def getFolderContents(self,rootPath):
		dirContents = []
		if os.path.exists(rootPath):
			for dirname, dirnames, filenames in os.walk(rootPath):
				for filename in filenames:
					dirContents.append(os.path.join(rootPath, filename))
		return dirContents

	def updateHelpText(self):
		contents = self.getFolderContents(self.getHelpDir(True))
		self.readAndPersistHelpContent(contents)
		contents = self.getFolderContents(self.getHelpDir(False))
		self.readAndPersistHelpContent(contents)

	def readAndPersistHelpContent(self,fileList):
		for fileName in fileList:
			f = open(fileName,'rU')
			contents = f.readlines()
			category = ntpath.basename(fileName).split('.')[0]
			self.persistHelpContents(category,contents)
			f.close()

	def persistHelpContents(self,category,contents):
		currentContent = ''
		marker = ''
		for each in contents:
			if each.strip().startswith('[') and each.strip().endswith(']'):
				if marker <> '' and currentContent <> '':
					self.saveHelpData(currentContent, category, marker)
				marker = each.strip()[1:len(each.strip())-1]
				currentContent = ''
			else:
				if not each.startswith("#"):
					currentContent += each
		self.saveHelpData(currentContent, category, marker)

	def saveHelpData(self,content, category, marker):
		if len(content.strip()) > 0:
			if marker == "Category":
				self.saveCategoryLevelHelp(category,content)
			else:
				self.saveFieldLevelHelp(marker,content)

	def saveCategoryLevelHelp(self,category,content):
		sql = "UPDATE cv_category SET help_text = %s WHERE code = %s"
		args = (content.strip(), category,)
		self.db.executeSQLCommand(sql,args)

	def saveFieldLevelHelp(self,fieldCode,content):
		sql = "UPDATE cv_field SET help_text = %s WHERE code = %s"
		args = (content.strip(), fieldCode,)
		self.db.executeSQLCommand(sql,args)

	def validRow(self,row):
		if not len(row) > 0:
			return False
		if row[0].startswith("#"):
			return False
		if len(row[0]) < 1:
			return False

		return True

	def getCode(self,instr):
		allowed = string.letters + string.digits
		returnVal = ""
		for each in instr:
			if allowed.find(each) > -1:
				returnVal += each
		return returnVal

	def getImportFile(self, fileName):
		mySite = self.site.replace('.','_')
		filepath = os.path.abspath(__file__).split("car")[0] + "car%sdata%scvMetaData%ssites%s%s%s" % (os.sep,os.sep,os.sep,os.sep,mySite,os.sep) + fileName
		if not os.path.exists(filepath):
			filepath = os.path.abspath(__file__).split("car")[0] + "car%sdata%scvMetaData%s" % (os.sep,os.sep,os.sep) + fileName
		f = open(filepath, 'rU')
		data = list(csv.reader(f, delimiter='\t'))
		f.close()
		return data

	def getHelpDir(self, isDefaultData = True):
		mySite = self.site.replace('.','_')
		if isDefaultData:
			dir = os.path.abspath(__file__).split("car")[0] + "car%sdata%scvMetaData%shelpText%s" % (os.sep,os.sep,os.sep,os.sep)
		else:
			dir = os.path.abspath(__file__).split("car")[0] + "car%sdata%scvMetaData%ssites%s%s%shelpText%s" % (os.sep,os.sep,os.sep,os.sep,mySite,os.sep,os.sep)
		return dir


	def getBool(self,instr):
		return stringUtils.interpretAsTrueFalse(instr)

	def connectToDatabase(self):
		connectionParms = dbConnParms.DbConnectionParms(self.host, self.port, self.dbname, self.user, self.password)
		self.db = sqlUtilities.SqlUtilities(connectionParms)


class DataLoadInterface:
	DESCR = '''Meta Data Load for CV'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=5432, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='mpsdev', help='database name (default=mpsdev')
		parser.add_option('-u', '--user', dest='user', default='mps', help='database user (default=mps)')
		parser.add_option('-w', '--password', dest='password', default='mps', help='database password')
		parser.add_option('-l', '--loadType', dest='loadType', default='all', help='load type. lookup, meta, all')
		parser.add_option('-s', '--site', dest='site', default='dev', help='folder in cvMetaData to load meta data from. Lookup data is the same across all sites.')

		return parser

	def run(self, options, args):
		try:
			cvLoad = CVLoad(options, args)
			cvLoad.process()
		except Exception, e:
			sys.exit(999)
			print e.message
		finally:
			if cvLoad:
				cvLoad.shutdown()


if __name__ == '__main__':
	logging.config.fileConfig(cStringIO.StringIO(MPSCore.core.constants.kDebugFormatFile))
	import MPSCore.utilities.sqlUtilities as sqlUtilities

	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
	sys.exit(0)