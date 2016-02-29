# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.emailService as emailSvc
import MPSCore.utilities.dateUtilities as dateUtils

class FileUpload(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setFileRepoSequenceList([])


	#   Getters/Setters.

	def getFileRepoSequenceList(self): return self.fileRepoSequenceList
	def setFileRepoSequenceList(self, _fileRepoSequenceList): self.fileRepoSequenceList = _fileRepoSequenceList


	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		fileRepoCache = self.getWorkflow().getFileRepoCache()
		self.setFileRepoSequenceList(fileRepoCache.get(self.getCode(),[]))


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			timezone = _sitePreferences.get('timezone', 'US/Eastern')
			format = _sitePreferences.get('ymdhmformat', '%m/%d/%Y %H:%M')
			jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))

			repoDict = {}
			repoDict['sequence_list'] = []
			max = int(self.getConfigDict().get('max','1'))
			if max < 1: max = 1
			for seqNbr in range(1,max+1):
				seqNbrDict = {}
				seqNbrDict['seq_nbr'] = str(seqNbr)
				seqNbrDict['current'] = {}
				seqNbrDict['versions'] = []
				uploadURL = '/appt/jobaction/file/upload/%s/%s/%i' % (jobActionIdStr, self.getCode(), seqNbr)
				seqNbrDict['upload_url'] = uploadURL
				repoDict['sequence_list'].append(seqNbrDict)

			for seqNbrDict in self.getFileRepoSequenceList():
				seqNbr = int(seqNbrDict.get('seq_nbr','99999'))
				if seqNbr <= max:
					currentDict = seqNbrDict.get('current',{})
					self.localizeDates(currentDict, timezone, format)
					argTuple = (jobActionIdStr, self.getCode(), seqNbr)
					currentDict['download_url'] = '/appt/jobaction/file/download/%s/%s/%i' % argTuple
					currentDict['delete_url'] = '/appt/jobaction/file/delete/%s/%s/%i' % argTuple
					repoDict['sequence_list'][seqNbr-1]['current'] = currentDict

					for version in seqNbrDict.get('versions',[]):
						self.localizeDates(version, timezone, format)
						version['download_url'] = '/appt/jobaction/file/download/%s/%s/%i/%s' % (jobActionIdStr, self.getCode(), seqNbr, str(version.get('version_nbr','0')))
					repoDict['sequence_list'][seqNbr-1]['versions'] = seqNbrDict.get('versions',[])

			disabled = self.standardTaskDisabledCheck()
			repoDict['disabled'] = disabled
			repoDict['activity_log'] = self.getTaskActivityLog(_sitePreferences)
			return repoDict

		return {}

	def localizeDates(self, _fileRepoDict, timezone, format):
		if _fileRepoDict:
			_fileRepoDict['created_display'] = self.localizeDate(_fileRepoDict.get('created',''), timezone, format)
			_fileRepoDict['updated_display'] = self.localizeDate(_fileRepoDict.get('updated',''), timezone, format)

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			if self.getFileRepoSequenceList():
				nbrWithCurrentFile = 0
				for seqNbrDict in self.getFileRepoSequenceList():
					if seqNbrDict.get('current',{}):
						nbrWithCurrentFile += 1

					min = int(self.getConfigDict().get('min','1'))
					if min < 1: min = 1
					if nbrWithCurrentFile >= min:
						return True
			return False
		return True
