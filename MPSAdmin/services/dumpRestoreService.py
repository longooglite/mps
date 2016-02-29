# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import os
import subprocess

from MPSAdmin.services.abstractAdminService import AbstractAdminService
import MPSAdmin.utilities.environmentUtils as envUtils


class DumpRestoreService(AbstractAdminService):
	logger = logging.getLogger(__name__)

	def __init__(self):
		AbstractAdminService.__init__(self)

	#   Dump a database.

	def dump(self, _dumpSite, _dumpFilename, _dbConnectionParms):

		#   Create/locate site folder.
		env = envUtils.getEnvironment()
		dumpFolderPath = env.getDumpFolderPath()
		siteFolderPath = os.path.join(dumpFolderPath, _dumpSite)
		self.createDumpFolder(dumpFolderPath)
		self.createDumpFolder(siteFolderPath)

		#   Use pg_dump to dump the postgres database.
		pgDumpBinaryPath = env.getPgdumpBinPath()
		pgDumpOutputFilePath = os.path.join(siteFolderPath, _dumpFilename)

		#   pg_dump -h <host> -p <port> -U <username> --no-password -f <outputfile> <databasename>
		args = []
		args.append(pgDumpBinaryPath)
		self._addPostgresArgs(args, _dbConnectionParms)
		args.append("-f")
		args.append(pgDumpOutputFilePath)
		args.append(_dbConnectionParms.getDbname())

		if self.logger.isEnabledFor(logging.INFO):
			self.logger.info(" ".join(args))
		subprocess.check_call(args)


	#   Restore a database.

	def restore(self, _restoreSite, _dumpSite, _dumpFilename, _dbConnectionParms):

		#   Find file to restore.
		env = envUtils.getEnvironment()
		dumpFolderPath = env.getDumpFolderPath()
		siteFolderPath = os.path.join(dumpFolderPath, _dumpSite)
		psqlInputFilePath = os.path.join(siteFolderPath, _dumpFilename)
		if not os.path.exists(psqlInputFilePath):
			raise Exception("File not found")

		#   dropdb -h <host> -p <port> -U <username> --no-password <databasename>
		#   createdb -h <host> -p <port> -U <username> --no-password <databasename>
		#   psql -h <host> -p <port> -U <username> --no-password <databasename> [with stdin=<dumpfile>]

		pgDropdbBinaryPath = env.getDropdbBinPath()
		pgCreatedbBinaryPath = env.getCreatedbBinPath()
		pgPsqlBinaryPath = env.getPsqlBinPath()

		args = []
		args.append(pgDropdbBinaryPath)
		self._addPostgresArgs(args, _dbConnectionParms)
		args.append(_dbConnectionParms.getDbname())

		if self.logger.isEnabledFor(logging.INFO):
			self.logger.info(" ".join(args))
		subprocess.call(args)

		args = []
		args.append(pgCreatedbBinaryPath)
		self._addPostgresArgs(args, _dbConnectionParms)
		args.append(_dbConnectionParms.getDbname())

		if self.logger.isEnabledFor(logging.INFO):
			self.logger.info(" ".join(args))
		subprocess.check_call(args)

		args = []
		args.append(pgPsqlBinaryPath)
		self._addPostgresArgs(args, _dbConnectionParms)
		args.append(_dbConnectionParms.getDbname())

		if self.logger.isEnabledFor(logging.INFO):
			self.logger.info("%s %s" % (" ".join(args), psqlInputFilePath))

		f = None
		try:
			f = open(psqlInputFilePath, mode='r')
			subprocess.check_call(args, stdin=f)
		finally:
			if f:
				try: f.close()
				except Exception, e: pass

		migrationMessage = self.performMigration(_dumpSite,_dbConnectionParms)
		return migrationMessage


	def performMigration(self,_dumpSite,_dbConnectionParms):
		srcRootFolderPath = os.path.dirname(os.path.abspath(__file__)).split('MPSAdmin')[0]+'commands/'
		if _dumpSite == 'auth':
			srcRootBinPath = srcRootFolderPath + 'migrateAuth.py'
		else:
			srcRootBinPath = srcRootFolderPath + 'migrateClient.py'
		args=[]
		args.append('python')
		args.append(srcRootBinPath)
		args.append('migrate')
		args.append('-d')
		args.append(_dbConnectionParms.getDbname())
		args.append('-t')
		args.append(_dbConnectionParms.getHost())
		args.append('-p')
		args.append(str(_dbConnectionParms.getPort()))
		args.append('-u')
		args.append(_dbConnectionParms.getUsername())
		args.append('-w')
		args.append(_dbConnectionParms.getPassword())

		process = subprocess.Popen(args, stdout=subprocess.PIPE)
		out, err = process.communicate()
		if  process.returncode <> 0:
			return out
		return ""


	#   Delete a database dump file.

	def delete(self, _dumpSite, _dumpFilename):

		#   Find file to delete.
		env = envUtils.getEnvironment()
		dumpFolderPath = env.getDumpFolderPath()
		siteFolderPath = os.path.join(dumpFolderPath, _dumpSite)
		dumpFilePath = os.path.join(siteFolderPath, _dumpFilename)
		if not os.path.exists(dumpFilePath):
			raise Exception("File not found")

		if self.logger.isEnabledFor(logging.INFO):
			self.logger.info("remove %s" % (dumpFilePath,))

		os.remove(dumpFilePath)


	#   Get a listing of all dumped database files.

	def getDumpFileList(self):
		fileList = []
		env = envUtils.getEnvironment()
		dumpFolderPath = env.getDumpFolderPath()

		walker = os.walk(dumpFolderPath)
		for each3Tuple in walker:
			thisPath = each3Tuple[0]
			thisFileList = each3Tuple[2]
			if thisFileList:
				ignored, site = os.path.split(thisPath)
				for filename in thisFileList:
					if filename != '.DS_Store':
						key = "%s|%s" % (site, filename)
						fileList.append({ "site": site, "filename": filename, "key": key })

		return fileList


	#   Misc.

	def createDumpFolder(self, _path):
		try:
			os.makedirs(_path)
		except Exception, e:
			pass

	def _addPostgresArgs(self, _args, _dbConnectionParms):
		_args.append("-h")
		_args.append(_dbConnectionParms.getHost())
		_args.append("-p")
		_args.append(str(_dbConnectionParms.getPort()))
		_args.append("-U")
		_args.append(_dbConnectionParms.getUsername())
		_args.append('--no-password')
