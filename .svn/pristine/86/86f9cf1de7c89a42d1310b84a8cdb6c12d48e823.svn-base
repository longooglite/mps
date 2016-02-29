# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#	Class which holds database connection parameter primitives.

class DbConnectionParms():

	def __init__(self, host=None, port=None, dbname=None, username=None, password=None):
		self.setHost(None)
		self.setPort(None)
		self.setDbname(None)
		self.setUsername(None)
		self.setPassword(None)
	
		if host: self.setHost(str(host))
		if port: self.setPort(int(port))
		if dbname: self.setDbname(str(dbname))
		if username: self.setUsername(str(username))
		if password: self.setPassword(str(password))


	#	Accessors.
	
	def getHost(self): return self.host
	def getPort(self): return self.port
	def getDbname(self): return self.dbname
	def getUsername(self): return self.username
	def getPassword(self): return self.password
	
	def setHost(self, _host): self.host = _host
	def setPort(self, _port): self.port = _port
	def setDbname(self, _dbname): self.dbname = _dbname
	def setUsername(self, _username): self.username = _username
	def setPassword(self, _password): self.password = _password


#	Create a default global DbConnectionParms instance,
#   and provide methods to initialize and retrieve it.

gDefaultDbConnectionParms = None

def getDefaultDbConnectionParms():
	global gDefaultDbConnectionParms
	return gDefaultDbConnectionParms

def initDefaultDbConnectionParms(_host=None, _port=None, _dbname=None, _username=None, _password=None):
	global gDefaultDbConnectionParms
	gDefaultDbConnectionParms = DbConnectionParms(host=_host, port=_port, dbname=_dbname, username=_username, password=_password)
