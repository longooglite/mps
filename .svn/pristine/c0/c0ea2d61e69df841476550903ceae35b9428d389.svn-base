# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json
import urllib2
import urllib
import optparse
import time
from time import mktime
import datetime
import sys
import os
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import MPSCore.utilities.mpsMath as mpsMath

#pubmed db name and return max values were moved to prefs. Left here to satisfy command line interface.
pubMedConstants = {"kSummaryUrl":"http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
	"kSearchURL":"http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
	"kTerm":"term",
	"kId":"id",
	"kPubMedDB":"pubmed",
	"kPubMedCentralDB":"pmc",
	"uidReturnMax":"20000",
	"pubReturnMax":"25"}


class PublicationList():
	def __init__(self,_rawResponseDict):
		self.rawResult = _rawResponseDict.get('result',{})
		self.uids = self.rawResult.get('uids',[])
		self.publications = []

	def getPublications(self):
		return self.publications

	def parsePublications(self):
		for uid in self.uids:
			publicationDict = self.rawResult.get(uid,{})
			publication = Publication(publicationDict)
			publication.parsePublications()
			self.publications.append(publication)

###################################################

class Publication():
	def __init__(self, publicationDict):
		self._publicationDict = publicationDict
		self.authors = []
		self.articleIds = []
		self.attributes = []
		self.history = []
		self.languages = []
		self.doccontriblist = []
		self.pubType = []
		self.references = []
		self.availablefromurl = ''
		self.bookname = ''
		self.booktitle = ''
		self.chapter = ''
		self.docdate = ''
		self.doctype = ''
		self.edition = ''
		self.locationid = ''
		self.epubdate = ''
		self.essn = ''
		self.fulljournalname = ''
		self.issn = ''
		self.issue = ''
		self.lastauthor = ''
		self.locationlabel = ''
		self.medium = ''
		self.nlmuniqueid = ''
		self.pages = ''
		self.pmcrefcount = ''
		self.publisherlocation = ''
		self.publishername = ''
		self.pubstatus = ''
		self.recordstatus = ''
		self.reportnumber = ''
		self.sortfirstauthor = ''
		self.sortpubdate = ''
		self.sorttitle = ''
		self.source = ''
		self.srcdate = ''
		self.title = ''
		self.uid = ''
		self.vernaculartitle = ''
		self.viewcount = ''
		self.volume = ''

	def parsePublications(self):
		self.parseAuthors()
		self.parseArticleIds()
		self.parseHistory()
		self.attributes = self._publicationDict.get('attributes',[])
		self.languages = self._publicationDict.get('lang',[])
		self.doccontriblist = self._publicationDict.get('doccontriblist',[])
		self.pubType = self._publicationDict.get('pubtype',[])
		self.references = self._publicationDict.get('references',[])
		###### single attributes ######
		self.availablefromurl = self._publicationDict.get('availablefromurl','')
		self.bookname = self.cleanseStr(self._publicationDict.get('bookname',''))
		self.booktitle = self.cleanseStr(self._publicationDict.get('booktitle',''))
		self.chapter = self.cleanseStr(self._publicationDict.get('chapter',''))
		self.docdate = self._publicationDict.get('docdate','')
		self.doctype = self._publicationDict.get('doctype','')
		self.edition = self.cleanseStr(self._publicationDict.get('edition',''))
		self.locationid = self._publicationDict.get('locationid','')
		self.epubdate = self._publicationDict.get('epubdate','')
		self.essn = self._publicationDict.get('essn','')
		self.fulljournalname = self.cleanseStr(self._publicationDict.get('fulljournalname',''))
		self.issn = self._publicationDict.get('issn','')
		self.issue = self.cleanseStr(self._publicationDict.get('issue',''))
		self.lastauthor = self.cleanseStr(self._publicationDict.get('lastauthor',''))
		self.locationlabel = self._publicationDict.get('locationlabel','')
		self.medium = self._publicationDict.get('medium','')
		self.nlmuniqueid = self._publicationDict.get('nlmuniqueid','')
		self.pages = self._publicationDict.get('pages','')
		self.pmcrefcount = self._publicationDict.get('pmcrefcount','')
		self.publisherlocation = self._publicationDict.get('publisherlocation','')
		self.publishername = self.cleanseStr(self._publicationDict.get('publishername',''))
		self.pubstatus = self._publicationDict.get('pubstatus','')
		self.recordstatus = self._publicationDict.get('recordstatus','')
		self.reportnumber = self._publicationDict.get('reportnumber','')
		self.sortfirstauthor = self._publicationDict.get('sortfirstauthor','')
		self.sortpubdate = self._publicationDict.get('sortpubdate','')
		self.sorttitle = self._publicationDict.get('sorttitle','')
		self.source = self._publicationDict.get('source','')
		self.srcdate = self._publicationDict.get('srcdate','')
		self.title = self.cleanseStr(self._publicationDict.get('title',''))
		self.uid = self._publicationDict.get('uid','')
		self.vernaculartitle = self.cleanseStr(self._publicationDict.get('vernaculartitle',''))
		self.viewcount = self._publicationDict.get('viewcount','')
		self.volume = self._publicationDict.get('volume','')

	def serializePublication(self):
		data = []
		data.append(self.jsonify(self.articleIds))
		data.append(json.dumps(self.attributes))
		data.append(self.jsonify(self.authors))
		data.append(self.availablefromurl)
		data.append(self.bookname)
		data.append(self.booktitle)
		data.append(self.chapter)
		data.append(json.dumps(self.doccontriblist))
		data.append(self.parseDate(self.docdate,"????")) #dunno what format. Have not seen data with this filled in
		data.append(self.doctype)
		data.append(self.edition)
		data.append(self.locationid)
		data.append(self.parseDate(self.epubdate,"%Y %b %d"))
		data.append(self.essn)
		data.append(self.fulljournalname)
		data.append(self.jsonify(self.history))
		data.append(self.issn)
		data.append(self.issue)
		data.append(json.dumps(self.languages))
		data.append(self.lastauthor)
		data.append(self.locationlabel)
		data.append(self.medium)
		data.append(self.nlmuniqueid)
		data.append(self.pages)
		data.append(self.pmcrefcount)
		data.append(self.publisherlocation)
		data.append(self.publishername)
		data.append(self.pubstatus)
		data.append(json.dumps(self.pubType))
		data.append(self.recordstatus)
		data.append(json.dumps(self.references))
		data.append(self.reportnumber)
		data.append(self.sortfirstauthor)
		data.append(self.sorttitle)
		data.append(self.source)
		data.append(self.parseDate(self.srcdate,"????")) #dunno what format. Have not seen data with this filled in
		data.append(self.title)
		data.append(self.uid)
		data.append(self.vernaculartitle)
		data.append(self.viewcount)
		data.append(self.volume)
		return data

	def cleanseStr(self,_str):
		someString = _str
		if someString is not None:
			if isinstance(someString,unicode) or isinstance(someString,str):
				someString.replace("&amp;","&")
		return someString

	def parseDate(self, stringValue, format):
		if format == "????":
			return None
		returnVal = None
		try:
			time_struct = time.strptime(stringValue,format)
			returnVal = datetime.date(time_struct.tm_year,time_struct.tm_mon,time_struct.tm_mday)
		except Exception,e:
			pass
		return returnVal

	def parseHistory(self):
		pubHist = self._publicationDict.get('history',[])
		for pubHistDict in pubHist:
			pubHist = PublicationHistory(pubHistDict)
			self.history.append(pubHist)

	def parseAuthors(self):
		authors = self._publicationDict.get('authors',[])
		for authorDict in authors:
			author = Author(authorDict)
			self.authors.append(author)

	def parseArticleIds(self):
		articleIds = self._publicationDict.get('articleids',[])
		for articleIdDict in articleIds:
			articleId = ArticleId(articleIdDict)
			self.articleIds.append(articleId)

	def jsonify(self,dictList):
		aList = []
		for each in dictList:
			aList.append(each.originalDict)
		return json.dumps(aList)

class Author():
	def __init__(self, authorDict):
		self.originalDict = authorDict
		self.authtype = authorDict.get('authtype','')
		self.clusterid = authorDict.get('clusterid','')
		self.name = authorDict.get('name','')

class ArticleId():
	def __init__(self, articleDict):
		self.originalDict = articleDict
		self.idtype = articleDict.get('idtype','')
		self.idtypen = articleDict.get('idtypen','')
		self.value = articleDict.get('value','')

class PublicationHistory():
	def __init__(self, pubHistDict):
		self.originalDict = pubHistDict
		self.date = pubHistDict.get('date','')
		self.pubstatus = pubHistDict.get('pubstatus','')


class PubMedInterface():
	def doPubMedQuery(self, url, values):
		dictResult = {}
		try:
			data = urllib.urlencode(values)
			req = urllib2.Request(url, data)
			response = urllib2.urlopen(req)
			rawresult = response.read()
			dictResult = json.loads(rawresult)
		except Exception,e:
			pass
		finally:
			return dictResult

	def getSearchDict(self, key,value, retmax = '20', dbname = 'pubmed'):
		returnDict = {}
		returnDict['db'] = dbname
		returnDict['retmax'] = retmax
		returnDict['retmode'] = 'json'
		returnDict[key] = value
		return returnDict

	def getUIDSearchStrings(self,uidDict,querySize,alreadyImportedUids):
		alluidsList = uidDict.get('esearchresult',{}).get('idlist',[])
		uidList = self.minimizeListToNewResultsOnly(alluidsList,alreadyImportedUids)
		returnVal = []
		searchString = ''
		queryLengthCounter = 0
		for uid in uidList:
			queryLengthCounter += 1
			searchString += uid + ","
			if queryLengthCounter >= querySize:
				self.addToQueryList(searchString,returnVal)
				queryLengthCounter = 0
				searchString = ''
		self.addToQueryList(searchString,returnVal)
		return returnVal,len(uidList)

	def minimizeListToNewResultsOnly(self,allUidsList,alreadyImportedUidsList):
		searchList = []
		for id in allUidsList:
			if not id in alreadyImportedUidsList:
				searchList.append(id)
		return searchList

	def addToQueryList(self, searchString, searchList):
		if len(searchString) > 0:
			searchString = searchString[0:len(searchString)-1]
			searchList.append(searchString)

###################################################

class CommandLineInterface:
	DESCR = ''''''

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-a', '--affiliation', dest='affiliation', default="The University of Michigan", help='')
		parser.add_option('-f', '--first_name', dest='first_name', default="KC", help='')
		parser.add_option('-l', '--last_name', dest='last_name', default="Chung", help='')
		parser.add_option('-r', '--retmax', dest='retmax', default=pubMedConstants.get('pubReturnMax',''), help='')
		parser.add_option('-s', '--sleep', dest='sleep', default="0", help='0 by default')
		parser.add_option('-d', '--db', dest='dbname', default=pubMedConstants.get('kPubMedDB',""), help='0 by default')
		return parser


	def run(self, options, args):
		try:
			retmax = options.retmax
			sleep = mpsMath.getIntFromString(options.sleep)
			pubMedifier = PubMedInterface()
			db = options.dbname
			authorDict = {"first_name":options.first_name,"last_name":options.last_name,"affiliation":options.affiliation}
			values = pubMedifier.getSearchDict(pubMedConstants.get('kTerm',''), authorDict,pubMedConstants.get('uidReturnMax',''),db)
			uidDictResult = pubMedifier.doPubMedQuery(pubMedConstants.get('kSearchURL',''), values)

			uidList = pubMedifier.getUIDSearchStrings(uidDictResult,mpsMath.getIntFromString(retmax),[])

			counter = 0
			for queryStr in uidList:
				time.sleep(sleep)
				values = pubMedifier.getSearchDict(pubMedConstants.get('kId',''), queryStr, retmax, db)

				dictResult = pubMedifier.doPubMedQuery(pubMedConstants.get('kSummaryUrl',''), values)
				publicationList = PublicationList(dictResult)
				publicationList.parsePublications()
				for pub in publicationList.getPublications():
					counter += 1
					print "Query Result: %i" % (counter)
					print "Essn %s Publication Date %s" % (pub.essn,pub.epubdate)
					for type in pub.pubType:
						print "Publication Type: %s" % (type)
					print "Title: %s" % (pub.title)
					print "Journal Name: %s" % (pub.fulljournalname)
					for auth in pub.authors:
						print auth.name
					print ""
		except Exception,e:
			pass

if __name__ == '__main__':
	authorSearchInterface = CommandLineInterface()
	parser = authorSearchInterface.get_parser()
	(options, args) = parser.parse_args()
	authorSearchInterface.run(options, args)

