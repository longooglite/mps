# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCV.core.cvSQL as cvSQL
import MPSCV.core.metaSQL as metaSQL
import MPSCore.utilities.stringUtilities as stringUtilities
import MPSCore.utilities.coreEnvironmentUtils as coreEnvUtils
import MPSCV.utilities.publicationImport as pubImport
from MPSCV.utilities.publicationImport import kImportTypePubMed
from MPSCV.services import cvService as cvSVC
import json

class PubMedService():


	def __init__(self,_dbConnection,cv_id = None,pubmeddb = '',pubmedUIDReturnMax = '',pubmedPubReturnMax = '',searchKey=''):
		self.cv_id = cv_id
		self.dbConnection = _dbConnection
		self.importType = kImportTypePubMed
		self.pubmeddb = pubmeddb
		self.uIdReturnMax = pubmedUIDReturnMax
		self.pubReturnMax = pubmedPubReturnMax
		self.searchKey = searchKey

	def updatePubMedSearchKey(self, connection, person, authorsearchkey):
			if person[0].get('pubmedsearchkey','') <> authorsearchkey:
				oldSearchKey = person[0].get('pubmedsearchkey','')
				cvSQL.updatePubMedSearchKey(connection, person[0].get('id',-1), authorsearchkey)
				cvSQL.removeNonReviewedPubsOnAuthorChange(connection,oldSearchKey,person[0].get('id',-1))

	def getPubMedData(self,authorSearchDict):
		importer = pubImport.PublicationImport(self.dbConnection,kImportTypePubMed, self.cv_id, authorSearchDict, self.pubmeddb, self.uIdReturnMax, self.pubReturnMax)
		alreadyImportedPubs = self.listify(cvSQL.getPubMedImportedUids(self.dbConnection,self.cv_id))
		rawData,total = importer.doImport(alreadyImportedPubs)
		self.importPubMedData(rawData,self.searchKey)
		rawPubs = cvSQL.getPubMedPublications(self.dbConnection,self.cv_id)
		mine,notmine,notreviewed = self.buckettizeRawPubs(rawPubs)
		return mine,notmine,notreviewed,str(len(rawPubs)),total

	def getNbrPubsAvailable(self,authorSearchDict):
		importer = pubImport.PublicationImport(self.dbConnection,kImportTypePubMed, self.cv_id, authorSearchDict, self.pubmeddb, self.uIdReturnMax, self.pubReturnMax)
		alreadyImportedPubs = self.listify(cvSQL.getPubMedImportedUids(self.dbConnection,self.cv_id))
		nbrAvailable = importer.getNbrPubsAvailable(alreadyImportedPubs)
		return nbrAvailable

	def prepopulatePubMedData(self):
		rawPubs = cvSQL.getPubMedPublications(self.dbConnection,self.cv_id)
		mine,notmine,notreviewed = self.buckettizeRawPubs(rawPubs)
		return mine,notmine,notreviewed,str(len(rawPubs))

	def buckettizeRawPubs(self,rawPubs):
		mine, notmine, notreviewed = [],[],[]
		for each in rawPubs:
			self.synopsize(each)
			if not each.get('reviewed',False):
				notreviewed.append(each)
			elif each.get('reviewed',False) and each.get('claimed',False):
				mine.append(each)
			elif each.get('reviewed',False) and not each.get('claimed',False):
				notmine.append(each)
		return mine,notmine,notreviewed

	def synopsize(self,publication):
		if len(publication.get('booktitle','')) > 0:
			publication['synopsis'] = publication.get('booktitle','')
		else:
			authorList = self.getAuthorNameList(publication.get('authors',''))
			publication['synopsis'] = "%s, title: %s, volume: %s, issue: %s pages: %s authors: %s" % (publication.get('fulljournalname',''),
			                                                                                     publication.get('title',''),
			                                                                                     publication.get('volume',''),
			                                                                                     publication.get('issue',''),
			                                                                                     publication.get('pages',''),
			                                                                                     authorList)
			publication['pubauthornames'] = authorList
			publication['pubfulljournalname'] = publication.get('fulljournalname','')
			publication['pubtitle'] = publication.get('title','')
			publication['pubvolume'] = publication.get('volume','')
			publication['pubissue'] = publication.get('issue','')
			publication['pubpages'] = publication.get('pages','')
			publication['pubdate'] = ''
			pubDate = publication.get('epubdate', '')
			if pubDate is not None:
				if pubDate.month is not None:
					publication['pubdate'] = str(pubDate.month)
				if pubDate.year is not None:
					publication['pubdate'] = str(publication['pubdate'] + '/' + str(pubDate.year))
			publication['pubid'] = publication.get('uid', '')



	def getAuthorNameList(self,jsonStr):
		authors = json.loads(jsonStr)
		returnVal = ''
		for author in authors:
			name = author.get('name','')
			returnVal += name + ", "
		if len(returnVal) > 0:
			returnVal = returnVal[0:len(returnVal)-2]
		return returnVal.encode('ascii','replace')

	def listify(self,uidDictList):
		returnVal = []
		for each in uidDictList:
			returnVal.append(each.get('uid',''))
		return returnVal

	def tisMine(self,pubmed_uid,value):
		pass

	def importPubMedData(self,pubData,authorSearchDict):
		if len(pubData) > 0:
			now = coreEnvUtils.CoreEnvironment().formatUTCDate()
			pubimportResult = cvSQL.createPubImportHeader(self.dbConnection,self.cv_id, now)
			if len(pubimportResult) > 0:
				pubimportId = pubimportResult[0].get('id',-1)
				didInsert = False
				if pubimportId > -1:
					for pub in pubData:
						didInsert = cvSQL.importPubMedData(self.dbConnection, pubimportId, self.cv_id, pub.serializePublication(), now, pub.uid,authorSearchDict)
					if didInsert:
						self.dbConnection.executeSQLCommand("COMMIT;", ())
					else:
						cvSQL.removePubHeader(self.dbConnection,pubimportId)

	def persistPubOwnership(self, connection,cv_id,mine,notmine,notreviewed):
		now = coreEnvUtils.CoreEnvironment().formatUTCDate()
		cvSQL.persistMine(connection,now,cv_id,mine)
		notMineList = []
		for each in notmine:
			notMineList.append(each.get('uid',''))
		inClause = stringUtilities.getSQLInClause(notMineList)
		if inClause <> "":
			cvSQL.persistNotMine(connection,now,cv_id,inClause)
		inClause = stringUtilities.getSQLInClause(notreviewed)
		if inClause <> "":
			cvSQL.persistNotReviewed(connection,now,cv_id,inClause)

	def getCategories(self,categoryCodes):
		inClause = stringUtilities.getSQLInClause(categoryCodes)
		return metaSQL.getSpecificCategories(self.dbConnection,inClause)

	def persistPubsToCV(self,connection,pubmedmapping,cv_id,mine,notmine,cv_owner,loggedInUser):
		uidCodeInList = self.buildUIDInList(pubmedmapping)
		for each in mine:
			mapping = self.getPubMedCategoryMapping(each.get('pubcat',{}),pubmedmapping)
			if mapping <> {}:
				dataElements = mapping.get('dataElements',{})
				uidCode = dataElements.get('uid')
				pubExistsQry = cvSQL.rowExistsForPubMedID(connection,cv_id,uidCodeInList,each['uid'])
				doInsert = False
				if pubExistsQry:
					if not cvSQL.rowExistsForCategoryAndAttributeValue(connection,cv_id,uidCode,mapping.get('categoryCode',''),each['uid']):
						cvSQL.deletePubMedPublication(connection,cv_id,uidCodeInList,each['uid'])
						doInsert = True
				else:
					doInsert = True
				if doInsert:
					insertList = self.getPublicationAttributes(connection,mapping,each['uid'],cv_id)
					rowDict = {"exclude_from_cv_val":False}
					cvSVC.saveRowData(connection, 'default', cv_owner, rowDict, insertList, [], loggedInUser)
		for each in notmine:
			mapping = self.getPubMedCategoryMapping(each.get('pubcat',{}),pubmedmapping)
			if mapping <> {}:
				dataElements = mapping.get('dataElements',{})
				uidCode = dataElements.get('uid')
				pubExistsQry = cvSQL.rowExistsForPubMedID(connection,cv_id,uidCodeInList,each['uid'])
				if pubExistsQry:
					cvSQL.deletePubMedPublication(connection,cv_id,uidCodeInList,each['uid'])

	def buildUIDInList(self,pubmedmapping):
		idList = []
		for map in pubmedmapping:
			dataElements = map.get('dataElements',{})
			if dataElements:
				if dataElements.has_key('uid'):
					value = dataElements['uid']
					if value:
						idList.append(value)
		return stringUtilities.getSQLInClause(idList,True)


	def getPublicationAttributes(self,connection,mapping,uidCode,cv_id):
		returnVal = []
		pubMedRow = cvSQL.getPubMedImportRow(connection,uidCode,cv_id)
		if pubMedRow <> []:
			dataElements = mapping.get('dataElements')
			for key in dataElements:
				cvFieldCode = dataElements.get(key,'')
				if cvFieldCode <> "":
					value = self.translateValue(key,pubMedRow[0].get(key,''))
					if value <> '':
						returnVal.append(tuple([cvFieldCode,value]))
		return returnVal

	def translateValue(self,key,value):
		if key == 'epubdate':
			if value is None:
				return ''
			datevalue = value.strftime('%Y-%m-%d')
			return datevalue
		elif key == 'authors':
			return self.translateAuthors(value)
		return value

	def translateAuthors(self,value):
		if value == '':
			return ''
		returnVal = ''
		authors = json.loads(value)
		for author in authors:
			returnVal += author.get('name','') + ", "
		if len(returnVal) > 0:
			returnVal = returnVal.strip()[0:len(returnVal.strip())-1]
		return returnVal

	def getPubMedCategoryMapping(self,categoryCode,pubmedmapping):
		for map in pubmedmapping:
			if map.get('categoryCode','') == categoryCode:
				return map
		return None
