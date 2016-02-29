# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import logging
import psycopg2
import psycopg2.extras

from MPSCore.utilities.exceptionWrapper import mpsExceptionWrapper

class SqlUtilities():
	logger = logging.getLogger(__name__)

	#	Utility class for SQL operations.
	
	def __init__(self, _dbConnectionParms):
		self.mpsConnection = None
		self.dbConnectionParms = _dbConnectionParms

	def executeSQLQuery(self, _qryStr, _args=()):
		cur = None
		qryStr = str(_qryStr)
		try:
			cur = self.getMpsConnection().cursor(cursor_factory=psycopg2.extras.RealDictCursor)
			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.debug(cur.mogrify(qryStr, _args))
			cur.execute(qryStr, _args)
			return cur.fetchall()
		finally:
			if cur is not None:
				cur.close()
	
	def executeSQLCommand(self, _commandStr, _args=(), doCommit = True):
		cur = None
		commandStr = str(_commandStr)
		try:
			cur = self.getMpsConnection().cursor()
			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.debug(cur.mogrify(commandStr, _args))
			cur.execute(commandStr, _args)
			if doCommit:
				self.performCommit()
		finally:
			if cur is not None:
				cur.close()

	@mpsExceptionWrapper("Unable to establish connection to customer database ")
	def getMpsConnection(self):
		if self.mpsConnection:
			return self.mpsConnection

		self.mpsConnection = psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" %
		    (self.dbConnectionParms.getDbname(),
		     self.dbConnectionParms.getUsername(),
		     self.dbConnectionParms.getPassword(),
		     self.dbConnectionParms.getHost(),
		     self.dbConnectionParms.getPort()))
		return self.mpsConnection

	@mpsExceptionWrapper("Unable to perform database command")
	def performCommit(self):
		if self.mpsConnection:
			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.debug("commit")
			self.mpsConnection.commit()

	@mpsExceptionWrapper("Unable to perform database command")
	def performRollback(self):
		if self.mpsConnection:
			if self.logger.isEnabledFor(logging.DEBUG):
				self.logger.debug("rollback")
			self.mpsConnection.rollback()

	def closeMpsConnection(self):
		if self.mpsConnection:
			self.mpsConnection.close()
			self.mpsConnection = None

	def getRowCount(self, _tableName, _whereClause=None):
		sql = []
		sql.append("SELECT COUNT(*) AS count FROM ")
		sql.append(_tableName)
		if _whereClause and len(_whereClause) > 0:
			sql.append(" WHERE ")
			sql.append(_whereClause)
		sql.append(";")
		query = "".join(sql)
		
		countDict = self.executeSQLQuery(query)
		if countDict and len(countDict) > 0 and 'count' in countDict[0]:
			return int(countDict[0]['count'])
		return 0

	def getLastSequenceNbr(self, _tableName):
		sql = '''SELECT CURRVAL('%s_id_seq') AS currval''' % _tableName
		currvalDict = self.executeSQLQuery(sql)
		if currvalDict and len(currvalDict) > 0 and 'currval' in currvalDict[0]:
			return int(currvalDict[0]['currval'])
		return 0

	def qEsc(self,instr=' '):
		if instr == '' or instr is None:
			instr = ' '
		outstr = ''
		if len(instr)>0:
			instr = instr.replace('\\', '-')
			outstr = instr.replace("'", "\\'")
		return outstr
