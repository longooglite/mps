# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import os

import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.services.packetService as packetSvc
import MPSAppt.services.fileRepoService as fileRepoSvc
import MPSAppt.services.uberDisplayService as uberDisplaySvc
import MPSAppt.core.constants as constants
import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.mpsMath as math

class PacketMaster:
	def __init__(self, _connection, _packetCode, packetTitle, _workflow, _templateLoader, _templateName, _context, _configDict):
		self.dbConnection = _connection
		self.packetCode = _packetCode
		self.workflow = _workflow
		self.env = envUtils.getEnvironment()
		self.packetPath = self.env.createGeneratedOutputFileInFolderPath(packetTitle + '.pdf')
		self.templateLoader = _templateLoader
		self.templateName = _templateName
		self.context = _context
		self.configDict = _configDict

	def generatePacket(self):
		packetMeta = packetSvc.getPacketMeta(self.dbConnection,self.packetCode)
		self.populateSequenceNbrPossibilities(packetMeta)
		self.populateContent(packetMeta)
		self.writeContentToTmp(packetMeta)
		tocFullPath = ''
		bookmarkList = []
		if not self.configDict.get('omitTOC',False):
			tocFullPath,tocPages,bookmarkList = self.generateTOC(packetMeta,1)
			if tocPages <> 1:
				#if toc renders > 1 page, rebuild toc, now that we know that fact, and adjust page offset
				tocFullPath,tocPages,bookmarkList = self.generateTOC(packetMeta,tocPages)
		self.mergeContents(tocFullPath,packetMeta,bookmarkList)

	def generateTOC(self,packetMeta,tocOffset=1):
		tocList = []
		bookmarkList = [{"description":"Table of Contents","page":1,"children":[]}]
		pageNumber = 1
		totalPages = 0
		for packetgroup in packetMeta.get('groups',[]):
			description = packetgroup.get('descr','')
			pages = 0
			itemBookmarks = []
			for item in packetgroup.get('items',[]):
				pages += item.get('pages',0)
				totalPages += item.get('pages',0)
					#if item.get('pages',0) > 0:
					# taking children out since recent sig pubs all have the same description and therefore look stoopid
					# if len(packetgroup.get('items',1)) > 1:
					# 	itemBookmarks.append({"description":item.get('descr',''),"page":totalPages+tocOffset})
			if pages > 0:
				if self.configDict.get('add_num_pages_toc_specifier',False):
					if pages == 1:
						description += " (1 page)"
					else:
						description += " (%i pages)" % (pages)
				tocList.append({"description":description,"page":str(pageNumber+tocOffset)})
				bookmarkList.append({"description":description,"page":pageNumber+tocOffset,"children":itemBookmarks})
				pageNumber += pages
		if totalPages > 0:
			if self.configDict.get('add_last_page_toc_entry',False):
				tocList.append({"description":"Last Page","page":str(pageNumber),"children":[]})
		self.context["toc"] = tocList
		pdfhtml = self.templateLoader._create_template(self.templateName).generate(context=self.context)
		pdffilename,pdffullPath = pdfUtils.createPDFFromHTML(pdfhtml, self.env,"",False,'packet_')
		pages = pdfUtils.getPageCountAndNormalizePDFContent(pdffullPath)
		return pdffullPath,pages,bookmarkList


	def mergeContents(self,tocFullPath,packetMeta,bookmarks):
		merger = PdfFileMerger()
		if not self.configDict.get('omitTOC',False):
			merger.append(open(tocFullPath),tocFullPath)
		if packetMeta:
			for packetgroup in packetMeta.get('groups',[]):
				for item in packetgroup.get('items',[]):
					if item.get('file_name',''):
						merger.append(open(item.get('file_name','')),item.get('file_name',''))
		if not self.configDict.get('omitTOC',False):
			merger.bookmarks = []
			for bookmark in bookmarks:
				parent_ref = merger.addBookmark(bookmark.get("description",''),bookmark.get('page',1)-1)
				for child in bookmark.get("children",[]):
					merger.addBookmark(child.get("description",''),child.get('page',1)-1,parent_ref)
		output = open(self.packetPath, "wb")
		merger.write(output)
		output.close()
		merger.close()


	def writeContentToTmp(self,packetMeta):
		if packetMeta:
			for packetgroup in packetMeta.get('groups',[]):
				for item in packetgroup.get('items',[]):
					item['file_name'] = None
					item['pages'] = 0
					contentDict = item.get('content',None)
					if contentDict and contentDict.get('content',''):
						#write to tmp, keep track of location
						item['file_name'] = self.env.createGeneratedOutputFilePath('file_', '.pdf')
						f = open(item['file_name'],'wb')
						f.write(bytearray(contentDict.get('content','')))
						f.flush()
						f.close()
						item['pages'] = contentDict.get('pages',0)


	def populateContent(self,packetMeta):
		jobTaskCache = self.workflow.getJobTaskCache()
		if packetMeta:
			for packetgroup in packetMeta.get('groups',[]):
				for item in packetgroup.get('items',[]):
					item['content'] = None
					item['file_name'] = None
					if item.get('is_artifact',False):
						self.getArtifact(item)
					container = self.workflow.getContainer(item.get('item_code',None))
					if container:
						jobTaskDict = jobTaskCache.get(container.getCode())
						if jobTaskDict:
							className = container.getClassName()
							if className == constants.kContainerClassFileUpload:
								item['content'] = fileRepoSvc.FileRepoService(self.dbConnection).getFileRepoContent(jobTaskDict,item['seq'])
							elif className == constants.kContainerClassUberForm:
								item['content'] = uberDisplaySvc.UberDisplayService(self.dbConnection).getPacketContent(self.workflow,self.templateLoader,jobTaskDict.get('task_code',''),self.env,self.context)
							elif not item['content']:
								item['content'] = container.getContent()

	def getArtifact(self,artifactItem):
		params = {}
		params['context'] = self.context
		params['env'] = self.env
		params['dbConnection'] = self.dbConnection
		params['workflow'] = self.workflow
		params['packetCode'] = self.packetCode
		params['templateLoader'] = self.templateLoader
		params['config'] = artifactItem.get('artifact_config_dict')
		importString = "from MPSAppt.modules.%s import Artifact" % (artifactItem.get('item_code',''))
		exec importString
		artifact = eval('Artifact(params)')
		returnValue = artifact.getContent()
		artifactItem['content'] = {'content':returnValue.get('content',''),'pages':returnValue.get('pages',0)}
		artifactItem['descr'] = returnValue.get('descr','')
		config = eval(params.get('config',{}))
		if config.get('task_code',''):
			artifactItem['item_code'] = config.get('task_code','')


	def populateSequenceNbrPossibilities(self,packetMeta):
		if packetMeta:
			for packetgroup in packetMeta.get('groups',[]):
				newItems = []
				for taskItem in packetgroup.get('items',[]):
					taskItem['seq'] = 1
					taskItem['descr'] = ''
					newItems.append(taskItem)
					container = self.workflow.getContainer(taskItem.get('item_code',None))
					if container:
						taskItem['descr'] = container.containerDict.get('descr','')
						maxSeq = math.getIntFromString(container.getConfigDict().get('max',1))
						if maxSeq > 1:
							currentSeq = 2
							while currentSeq <= maxSeq:
								newItem = taskItem.copy()
								newItem['seq'] = currentSeq
								newItems.append(newItem)
								currentSeq += 1
				packetgroup['items'] = newItems


	def getUxPath(self):
		return self.env.getUxGeneratedOutputFilePath(self.packetPath)