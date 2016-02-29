# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.core.constants as constants
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.core.sql.fileRepoSQL as frSQL


class FileRepoService(AbstractTaskService):
	def __init__(self, _connection):
		AbstractTaskService.__init__(self, _connection)

	def getFileRepo(self, _jobTaskDict, _seqNbr):
		return frSQL.getFileRepo(self.connection, _jobTaskDict, _seqNbr)

	def getFileRepoForVersion(self, _jobTaskDict, _seqNbr, _versionNbr):
		return frSQL.getFileRepoForVersion(self.connection, _jobTaskDict, _seqNbr, _versionNbr)

	def getLastFileRepo(self, _jobTaskDict, _seqNbr):
		return frSQL.getLastFileRepo(self.connection, _jobTaskDict, _seqNbr)

	def getFileRepoForJobAction(self, _jobActionId):
		return frSQL.getFileRepoForJobAction(self.connection, _jobActionId)

	def getFileRepoContent(self, _jobTaskDict, _seqNbr):
		return frSQL.getFileRepoContent(self.connection, _jobTaskDict, _seqNbr)

	def getFileRepoContentForVersion(self, _jobTaskDict, _seqNbr, _versionNbr):
		return frSQL.getFileRepoContentForVersion(self.connection, _jobTaskDict, _seqNbr, _versionNbr)

	def obliterateFileRepoForSeqNbr(self, _fileRepoDict, doCommit=True):
		frSQL.obliterateFileRepoForSeqNbr(self.connection, _fileRepoDict, doCommit)

	def createFileRepo(self, _fileRepoDict, doCommit=True):
		frSQL.createFileRepo(self.connection, _fileRepoDict, doCommit)

	def updateFileRepo(self, _jobTaskDict, _fileRepoDict, doCommit=True):
		existingFileRepo = self.getLastFileRepo(_jobTaskDict, _fileRepoDict.get('seq_nbr', 1))

		try:
			if existingFileRepo:
				if not existingFileRepo.get('deleted', False):
					existingFileRepo['deleted'] = True
					self.setFileRepoDeleted(existingFileRepo, doCommit=False)
				_fileRepoDict['version_nbr'] = existingFileRepo.get('version_nbr',0) + 1
			else:
				_fileRepoDict['version_nbr'] = 1

			_fileRepoDict['deleted'] = False
			self.createFileRepo(_fileRepoDict, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleUpload(self, _jobActionDict, _jobTaskDict, _fileRepoDict, _container, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   Create/Update the File Repository.
			self.updateFileRepo(_jobTaskDict, _fileRepoDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbUpload
				logDict['item'] = _fileRepoDict.get('file_name', '')
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def deleteFileRepo(self, _jobTaskDict, _fileRepoDict, doCommit=True):
		existingFileRepo = self.getFileRepo(_jobTaskDict, _fileRepoDict.get('seq_nbr', 1))

		try:
			if existingFileRepo:
				existingFileRepo['deleted'] = True
				self.setFileRepoDeleted(existingFileRepo, doCommit=False)

				if doCommit:
					self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def handleDelete(self, _jobActionDict, _jobTaskDict, _fileRepoDict, _container, _profile, _now, _username, doCommit=True):
		try:
			#   Logging setup.
			logDict = {}
			logDict['logEnabled'] = _container.getIsLogEnabled()
			logDict['job_action_id'] = _jobTaskDict.get('job_action_id', None)
			logDict['job_task_id'] = _jobTaskDict.get('id', None)
			logDict['class_name'] = _container.getClassName()
			logDict['created'] = _now
			logDict['lastuser'] = _username

			#   'Delete' from the File Repository.
			self.deleteFileRepo(_jobTaskDict, _fileRepoDict, doCommit=False)

			#   Write the Job Action Log entry.
			if _container.getIsLogEnabled():
				logDict['verb'] = constants.kJobActionLogVerbDelete
				logDict['item'] = _fileRepoDict.get('file_name', '')
				logDict['message'] = _container.getLogMessage(logDict['verb'], logDict['item'])
				jobActionSvc.JobActionService(self.connection).createJobActionLog(logDict, doCommit=False)

			#   Common handler pre-commit activities.
			self.commmonHandlerPrecommitTasks(_jobActionDict, _jobTaskDict, _container, _profile, {}, _now, _username, doCommit=False)

			if doCommit:
				self.connection.performCommit()

		except Exception, e:
			try: self.connection.performRollback()
			except Exception, e1: pass
			raise e

	def setFileRepoDeleted(self, _fileRepoDict, doCommit=True):
		frSQL.setFileRepoDeleted(self.connection, _fileRepoDict, doCommit)

	def getFileRepoCache(self, _jobActionId):
		cache = {}
		lastTaskCode = None
		lastSeqNbr = None
		curTaskList = None
		curSeqNbrDict = None

		rowList = self.getFileRepoForJobAction(_jobActionId)
		for row in rowList:
			thisTaskCode = row.get('task_code','')
			if thisTaskCode != lastTaskCode:
				lastTaskCode = thisTaskCode
				curTaskList = []
				cache[thisTaskCode] = curTaskList
				lastSeqNbr = None
				curSeqNbrDict = None

			thisSeqNbr = row.get('seq_nbr','')
			if thisSeqNbr != lastSeqNbr:
				lastSeqNbr = thisSeqNbr
				curSeqNbrDict = {}
				curSeqNbrDict['seq_nbr'] = thisSeqNbr
				curSeqNbrDict['current'] = {}
				curSeqNbrDict['versions'] = []
				curTaskList.append(curSeqNbrDict)

			fileRepoDict = {}
			fileRepoDict['id'] = row.get('id',0)
			fileRepoDict['job_task_id'] = row.get('job_task_id',0)
			fileRepoDict['seq_nbr'] = str(row.get('seq_nbr',1))
			fileRepoDict['version_nbr'] = str(row.get('version_nbr',1))
			fileRepoDict['deleted'] = row.get('deleted',False)
			fileRepoDict['file_name'] = row.get('file_name','')
			fileRepoDict['content_type'] = row.get('content_type','')
			fileRepoDict['created'] = row.get('created','')
			fileRepoDict['updated'] = row.get('updated','')
			fileRepoDict['lastuser'] = row.get('lastuser','')

			if fileRepoDict['deleted']:
				curSeqNbrDict['versions'].append(fileRepoDict)
			else:
				curSeqNbrDict['current'] = fileRepoDict

		return cache
