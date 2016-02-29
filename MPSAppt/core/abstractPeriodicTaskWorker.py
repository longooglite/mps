# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import tornado.escape
import tornado.httpclient

import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSAppt.utilities.environmentUtils as envUtils

class AbstractPeriodicTaskWorker(object):

	def getSiteList(self):
		return self.postToAuthSvc('/sitelistbypass', {})

	def getProfileForSite(self, _siteCode):
		payload = {}
		payload['profileSite'] = _siteCode
		profile = self.postToAuthSvc("/siteprofiledetailbypass", payload)
		return profile

	def getConnectionParmsForSite(self, _profile):
		sitePrefsDict = _profile.get('sitePreferences',{})
		connectionParms = dbConnParms.DbConnectionParms(sitePrefsDict.get('dbhost',''),
														sitePrefsDict.get('dbport',''),
														sitePrefsDict.get('dbname',''),
														sitePrefsDict.get('dbusername',''),
														sitePrefsDict.get('dbpassword',''))
		return connectionParms

	def postToAuthSvc(self, _uri, _unJsonifiedPayload):
		response = ""
		authserviceurl = envUtils.getEnvironment().getAuthServiceUrl()
		http_client = tornado.httpclient.HTTPClient()
		try:
			jsonResponse = http_client.fetch(
				authserviceurl + _uri,
				method='POST',
				headers = {'Content-Type':'application/json'},
				body=tornado.escape.json_encode(_unJsonifiedPayload))
			response = tornado.escape.json_decode(jsonResponse.body)
		finally:
			http_client.close()

		return response
