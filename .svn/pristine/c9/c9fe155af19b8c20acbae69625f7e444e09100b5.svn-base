# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

'''
dataLoad.py

dataLoad is a non-cheesy little script to load data into Marta.

Usage:

$ python /path/to/dataLoad.py -d /path/to/dir/of/tab/delimited/files/

'''

import codecs
import datetime
import optparse
import os
import os.path
import sys
import string
from os.path import expanduser
import collections
import MySQLdb as mysqldb

schoolPaths = {"CMU":"/CAR/trunk/car/MartaLegacy/sites/CMU/DataLoad/"}

class DataLoad(object):
	# Initialization

	def __init__(self, options=None, args=None):
		self.srcPath = expanduser("~") + schoolPaths.get(options.school,"CMU")
		self.host = "localhost"
		self.port = 3306
		self.dbname = 'marta'
		self.user = 'marta'
		self.password = 'atram'
		self.host = options.host
		self.port = int(options.port)
		self.dbname = options.dbname
		self.user = options.user
		self.password = options.password

		self.db = self.connectToDatabase()

	#	Shutdown


	#	Execution

	def process(self):
		self.connectToDatabase()
		userGroupFile = self.loadFile('user_group.txt')
		self.loadUserGroups(userGroupFile)
		userDeptFile = self.loadFile('user_dept.txt')
		self.loadUserDepts(userDeptFile)
		userGroupFile.close()
		userDeptFile.close()

	def loadUserGroups(self,srcFile):

		groups = self.getGroups()

		processedHeader = False
		for line in srcFile:
			if len(line.strip()) == 0:
				continue
			splits = line.split("\t")
			if not processedHeader:
				processedHeader = True
				self.fileHeader = self.getFileHeader(splits)
			else:
				username = splits[self.fileHeader['USERID']]
				self.insertUserName(username)
				if self.getBool(splits[self.fileHeader['OFA']]):
					self.insertGroup(username,self.getGroupId('OFA',groups))
				if self.getBool(splits[self.fileHeader['DEPT']]):
					self.insertGroup(username,self.getGroupId('DEPT',groups))
				if self.getBool(splits[self.fileHeader['CBC_ADMIN']]):
					self.insertGroup(username,self.getGroupId('CBC_ADMIN',groups))
				if self.getBool(splits[self.fileHeader['CBC_VIEW']]):
					self.insertGroup(username,self.getGroupId('CBC_VIEW',groups))
				if self.getBool(splits[self.fileHeader['CBC_TEST']]):
					self.insertGroup(username,self.getGroupId('CBC_TEST',groups))

	def insertUserName(self,username):
		try:
			sql = "INSERT INTO users (username,password,enabled) VALUES (%s,%s,%s)"
			args = (username,"password",1,)
			self.executeStatement(sql,args)
		except:
			pass

	def insertGroup(self,username,group_id):
		try:
			sql = "INSERT INTO GROUP_MEMBERS (username,group_id) VALUES (%s,%s)"
			args = (username,group_id,)
			self.executeStatement(sql,args)
		except:
			pass

	def getGroupId(self,groupCode,groups):
		for each in groups:
			if each.get('GROUP_NAME','') == groupCode:
				return each.get('ID',-1)
		return None

	def getBool(self,_string):
		if _string:
			stringUC = _string.upper()
			if stringUC.startswith('1'): return True
			if stringUC.startswith('T'): return True
			if stringUC.startswith('Y'): return True
			if stringUC.startswith('ON'): return True
		return False

	def getGroups(self):
		sql = "SELECT * FROM GROUPS"
		args = ()
		return self.executeQuery(sql,args)

	def loadUserDepts(self,srcFile):

		processedHeader = False
		for line in srcFile:
			if len(line.strip()) == 0:
				continue
			splits = line.split("\t")
			if not processedHeader:
				processedHeader = True
				self.fileHeader = self.getFileHeader(splits)
			else:
				username = splits[self.fileHeader['USERID']]
				role = "ROLE_" + splits[self.fileHeader['DEPTID']]
				sql = "INSERT INTO authorities (username,authority) VALUES (%s,%s)"
				args = (username.strip(),role.strip())
				self.executeStatement(sql,args)

	def getFileHeader(self,header):
		indexes = {}
		counter = 0
		for each in header:
			indexes[each.strip()] = counter
			counter = counter + 1
		return indexes

	def loadFile(self,fileName):
		print "Loading %s" % (fileName)
		file = None
		try:
			file = codecs.open(self.srcPath + fileName, 'r', 'utf-8', errors='ignore')
		except Exception, e:
			sys.exit(1)
		return file

	def getLine(self,line):
		splits = line.split("\t")
		return splits


	def closeSourceFiles(self,srcFiles):
		try:
			for f in srcFiles:
				if f <> None:
					f.close()
		except:
			pass


	#	Database

	def getCursor(self):
		return self.db.cursor(mysqldb.cursors.DictCursor)

	def executeStatement(self, _stmt, _args=None):
		curs = None
		try:
			curs = self.getCursor()
			curs.execute(_stmt, _args)
			self.db.commit()
		finally:
			if curs:
				curs.close()

	def executeQuery(self, _query, _args=None):
		curs = None
		try:
			curs = self.getCursor()
			curs.execute(_query, _args)
			results = curs.fetchall()
			self.db.rollback()
			return results
		except Exception,e:
			pass
		finally:
			if curs:
				curs.close()

	def executeInsertReturnId(self, _stmt, _args=None):
		curs = None
		try:
			curs = self.getCursor()
			curs.execute(_stmt, _args)
			self.db.commit()
			curs.execute("SELECT LAST_INSERT_ID() AS ID")
			return curs.fetchone()['ID']
		except Exception,e:
			pass
		finally:
			if curs:
				curs.close()


	def connectToDatabase(self):
		self.db = mysqldb.connect(host=self.host, port=self.port, db=self.dbname, user=self.user, passwd=self.password)

class DataLoadInterface:
	DESCR = '''Good luck Jim.'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		parser.add_option('-s', '--school', dest='school', default="CMU", help='school name')
		parser.add_option('-t', '--host', dest='host', default='localhost', help='database host (default=localhost)')
		parser.add_option('-p', '--port', dest='port', default=3306, help='database port (default=3306)')
		parser.add_option('-d', '--dbname', dest='dbname', default='marta', help='database name (default=marta')
		parser.add_option('-u', '--user', dest='user', default='marta', help='database user (default=marta)')
		parser.add_option('-w', '--password', dest='password', default='atram', help='database password')
		parser.add_option('-x', '--destroy', dest='destroy', default='atram', help='database password')
		return parser

	def run(self, options, args):
		try:
			dataLoad = DataLoad(options, args)
			dataLoad.process()
		except Exception, e:
			for each in e.args:
				print each
		finally:
			pass

if __name__ == '__main__':
	dataLoadInterface = DataLoadInterface()
	parser = dataLoadInterface.get_parser()
	(options, args) = parser.parse_args()
	dataLoadInterface.run(options, args)
