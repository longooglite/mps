# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import sys
import os
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)
import time
import datetime
import optparse

import MPSCV.utilities.pubmed as pubmed
from MPSCV.utilities.pubmed import pubMedConstants
import MPSCore.utilities.mpsMath as mpsMath
import MPSCore.utilities.dbConnectionParms as dbConnParms

kImportTypePubMed = "pubmed"

class PublicationImport():
	def __init__(self,_dbConnection,_importType, _cv_id, _authorSearchDict, _pubmeddb, _pubmedUIDReturnMax, _pubmedPubReturnMax):
		rootFilePath = os.sep + "tmp" + os.sep
		self.cv_id = _cv_id
		self.pubmeddb = _pubmeddb
		self.pubmedUIDReturnMax = _pubmedUIDReturnMax
		self.pubmedPubReturnMax = _pubmedPubReturnMax
		self.authorSearchString = self.getAuthorSearchString(_importType,_authorSearchDict)
		self.importType = _importType
		self.dbConnection = _dbConnection
		self.fileName = rootFilePath + "pubmed_import%i_%s.csv" % (self.cv_id,str(datetime.datetime.now()))

	def getAuthorSearchString(self,importType,searchDict):
		returnVal = ''
		if importType == kImportTypePubMed:
			if searchDict.get('affiliation',''):
				returnVal = "(%s %s[Author] AND %s[Affiliation])" % (searchDict.get('last_name'),searchDict.get('first_name'),searchDict.get('affiliation',''))
			else:
				returnVal = "(%s %s[Author])" % (searchDict.get('last_name'),searchDict.get('first_name'))
			returnVal = returnVal.strip()
		return returnVal

	def doImport(self, alreadyImportedUidList = []):
		if self.importType == kImportTypePubMed:
			publications, total = self.getPubMedPublications(alreadyImportedUidList)
			return publications, total

	def getUIDSearchDict(self,pubMedInterface):
		return pubMedInterface.getSearchDict(pubMedConstants.get('kTerm',''),
                                       self.authorSearchString,
                                       self.pubmedUIDReturnMax,
                                       self.pubmeddb)


	def getPubMedPublications(self,alreadyImportedUidList):
		publications = []
		pubMedInterface = pubmed.PubMedInterface()
		values = self.getUIDSearchDict(pubMedInterface)

		uidDictResult = pubMedInterface.doPubMedQuery(pubMedConstants.get('kSearchURL',''),
		                                              values)

		uidList,uidcounter = pubMedInterface.getUIDSearchStrings(uidDictResult,
		                                              mpsMath.getIntFromString(self.pubmedPubReturnMax),
		                                              alreadyImportedUidList)

		if uidList <> []:
			for queryStr in uidList:
				values = pubMedInterface.getSearchDict(pubMedConstants.get('kId',''),
				                                       queryStr,
				                                       mpsMath.getIntFromString(self.pubmedPubReturnMax),
				                                       self.pubmeddb)

				dictResult = pubMedInterface.doPubMedQuery(pubMedConstants.get('kSummaryUrl',''), values)
				publicationList = pubmed.PublicationList(dictResult)
				publicationList.parsePublications()
				for pub in publicationList.getPublications():
					publications.append(pub)
				break
		return publications, uidcounter

	def getNbrPubsAvailable(self,alreadyImportedPubs):
		pubMedInterface = pubmed.PubMedInterface()
		values = self.getUIDSearchDict(pubMedInterface)

		uidDictResult = pubMedInterface.doPubMedQuery(pubMedConstants.get('kSearchURL',''),
		                                              values)
		uidList,uidcounter = pubMedInterface.getUIDSearchStrings(uidDictResult,
                                              mpsMath.getIntFromString(self.pubmedPubReturnMax),
                                              alreadyImportedPubs)

		return uidcounter

class DataLoadInterface:
	DESCR = '''Publication Load for pubmed and whatever else'''

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
			import MPSCore.utilities.sqlUtilities as sqlUtilities
			connectionParms = dbConnParms.DbConnectionParms(options.host, options.port, options.dbname, options.user, options.password)
			dbConnection = sqlUtilities.SqlUtilities(connectionParms)

			importer = PublicationImport(_dbConnection = dbConnection,
			                             _importType = kImportTypePubMed,
			                             _cv_id = 1,
			                             _authorSearchString = "Chung, Kevin",
			                             _pubmeddb = "pubmed",
			                             _pubmedUIDReturnMax = "20000",
			                             _pubmedPubReturnMax = "25")
			publications, total = importer.doImport()
			print publications, total
		except Exception, e:
			print e.message
		finally:
			dbConnection.closeMpsConnection()

if __name__ == '__main__':
	try:
		dataLoadInterface = DataLoadInterface()
		parser = dataLoadInterface.get_parser()
		(options, args) = parser.parse_args()
		dataLoadInterface.run(options, args)
	except Exception,e:
		pass
