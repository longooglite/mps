# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import json
import os
import tornado.escape
import tornado.httpclient
import tornado.web

import MPSCore.handlers.coreApplicationHandler as coreAppHandler
import MPSLogin.utilities.environmentUtils as envUtils

path = "%stmp%smaintenancemode.json" % (os.sep,os.sep)

class AbstractHandler(coreAppHandler.CoreApplicationHandler):

	def postToAuthSvcFromLogin(self, _uri, _unJsonifiedPayload, _exceptionOption):
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

		except Exception as e:
			if _exceptionOption == 'ignore':
				response = {}
			elif _exceptionOption == 'error':
				response = { 'error': e.message }
			else:
				raise e
		finally:
			http_client.close()

		return response

	def writeResponseHeaders(self):
		self.set_header('Content-Type','application/json')

	def isUnderMaintenance(self, site='all'):
		if os.path.exists(path):
			f = open(path)
			maintenanceData = json.load(f)
			if maintenanceData.get(site,'') <> '':
				return True
		return False

	def getMaintenanceModeMessage(self):
		if os.path.exists(path):
			f = open(path)
			maintenanceData = json.load(f)
			return maintenanceData.get('additionalMessage','')
		return ''

	def resolveHTMLPath(self, _htmlFilename):
		return os.path.join(envUtils.getEnvironment().getSrcRootFolderPath(), "MPSLogin", "html", _htmlFilename)
