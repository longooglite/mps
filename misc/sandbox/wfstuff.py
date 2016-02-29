import logging

import tornado.escape

import MPSAppt.handlers.abstractHandler as absHandler
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.core.workflow as wf
from misc.sandbox import phoneyBaloneyAnswerGenerator


class MainHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):
		self.verifyRequest()
		connection = self.getConnection()
		try:
			#   Render the page.
			userperms = []
			permA = {"appcode":"APPT","code":"viewA","descr":"View A"}
			permB = {"appcode":"APPT","code":"viewB","descr":"View B"}
			permC = {"appcode":"APPT","code":"viewC","descr":"View C"}
			userperms.append(permA)
			userperms.append(permB)
			userperms.append(permC)
			containerCode = "workflow_ABC"
			parameterBlock = {"userPermissions": userperms, "titleCode":"ClinicalClinicalInstructor", "jobActionId": 1}

			workflow = wf.Workflow(connection)
			workflow.buildWorkflow(containerCode, parameterBlock)

			context = self.getInitialTemplateContext(envUtils.getEnvironment())
#			context['workflow'] = { 'taskList': workflow.getWorkFlow() }
			context['status'] = workflow.computeStatus()

			self.render("appt.html", context=context, skin=context['skin'])
		finally:
			self.closeConnection()

class LogoutHandler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def get(self):
		try:
			self._getHandlerImpl()
		except Exception, e:
			self.handleGetException(e, self.logger)

	def _getHandlerImpl(self):

		#   Try to log out, no biggie if we can't.
		#   Redirect to Login page.
		try:
			payload = { 'mpsid': self.getCookie('mpsid') }
			self.postToAuthSvc("/logout", payload)
		except Exception:
			pass

		self.handleGetException(None, None)



class A_Handler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()

		phoneyBaloneyAnswerGenerator.toggleValue('taskA')

		responseDict = self.getPostResponseDict()
		responseDict['redirect'] = '/appt'
		self.write(tornado.escape.json_encode(responseDict))

class B_Handler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()

		phoneyBaloneyAnswerGenerator.toggleValue('taskB')

		responseDict = self.getPostResponseDict()
		responseDict['redirect'] = '/appt'
		self.write(tornado.escape.json_encode(responseDict))

class C_Handler(absHandler.AbstractHandler):
	logger = logging.getLogger(__name__)

	def post(self):
		try:
			self._postHandlerImpl()
		except Exception, e:
			self.handlePostException(e, self.logger)

	def _postHandlerImpl(self):
		self.writePostResponseHeaders()
		self.verifyRequest()

		phoneyBaloneyAnswerGenerator.toggleValue('taskC')

		responseDict = self.getPostResponseDict()
		responseDict['redirect'] = '/appt'
		self.write(tornado.escape.json_encode(responseDict))


#   All URL mappings for this module.
urlMappings = [
	(r'/appt', MainHandler),
	(r'/appt/logout', LogoutHandler),
	(r'/appt/a_task', A_Handler),
    (r'/appt/b_task', B_Handler),
	(r'/appt/c_task', C_Handler),

]


