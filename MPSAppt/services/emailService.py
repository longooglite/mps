# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email.mime.image import MIMEImage

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.positionService as positionSvc
import MPSAppt.services.personService as personSvc
import MPSAppt.services.jobActionService as jobActionSvc
import MPSAppt.core.sql.emailSQL as emSQL
import MPSAppt.utilities.environmentUtils as envUtils
import MPSAppt.core.constants as constants
import MPSCore.utilities.coreEnvironmentUtils as coreEnvUtils

kEmailFrom = "smartPath@mntnpass.com"

class EmailService(AbstractTaskService):
	def __init__(self, _connection, _jobActionDict, _jobTaskDict=None, _container=None, _profile=None, _username=None, _now=None, _alertConfigKeyName='alert', _emailConfigKeyName='emails'):
		AbstractTaskService.__init__(self, _connection)

		self.jobActionDict = _jobActionDict
		self.jobTaskDict = _jobTaskDict
		self.container = _container
		self.profile = _profile
		self.username = _username
		self.now = _now
		self.alertConfigKeyName = _alertConfigKeyName
		self.emailConfigKeyName = _emailConfigKeyName

	#   Administrative emails

	def prepareAndSendAdministrativeEmail(self,addresses,subjectLine,body):
		emailDict = self.getEmailDict(addresses, [], [], subjectLine, body)
		emailer = Emailer(emailDict)
		emailer.sendMail()


	#   Alert emails.

	def prepareAndSendAlertEmail(self, doCommit=True):
		alertConfig = self.container.getConfigDict().get(self.alertConfigKeyName, {})
		revisionsRequired = False
		if self.container.getClassName() == constants.kContainerClassApproval:
			if self.container.approvalDict.get('approval','') == constants.kApprovalRevisionsRequired:
				revisionsRequired = True
		bodyText = alertConfig.get('emailTextComplete',self.container.getDescr() + " - Completed")
		if revisionsRequired:
			bodyText = alertConfig.get('emailTextRevisions',self.container.getDescr() + " - Revisions Required")

		if alertConfig:
			if (self.container.isComplete()) or (revisionsRequired) or (alertConfig.get('alwaysSend', False)):
				addresses, ccAddresses, bccAddresses = self.getEmailAddresses(alertConfig, {})
				if addresses:
					subjectLine = self.appendPCN(bodyText)

					url = self.getAlertUrl()
					body = self.getAlertBody(subjectLine, url)

					emailDict = self.getEmailDict(addresses, ccAddresses, bccAddresses, subjectLine, body)
					self.persistAndSend(emailDict, doCommit)

	def appendPCN(self,subject):
		subjectLine = subject
		position = positionSvc.getPostionById(self.connection,self.jobActionDict.get('position_id',None))
		if position:
			subjectLine += " - %s" % (position.get('pcn',''))
		return subjectLine

	def getAlertUrl(self):
		return "%s/jobaction/%s" % (self.getBaseUrl(), str(self.jobActionDict.get('id',"")))

	def getAlertBody(self,body,url):
		#in order to put an image in a mail use,
		#<img src="cid:filename"/> in the email where filename is the name of the file. The email routine will add
		#the image to the email header using the filename as the id.
		#return '''<html><body><a href="%s">%s</a><img src="cid:testimage"/></body></html>''' % (url,body)
		return '''<html><body><a href="%s">%s</a></body></html>''' % (url,body)


	#   I-need-you-to-do-blah emails.

	def prepareAndSendDirectiveEmails(self, doCommit=True):
		emailList = self.container.getConfigDict().get(self.emailConfigKeyName ,[])
		if emailList:
			site = self.profile.get('siteProfile',{}).get('site','')
			emailContext = self.initializeEmailContext()
			self.container.extendEmailContext(emailContext)

			for emailConfig in emailList:
				if self.wf_dependencySatisified(emailConfig):
					addresses, ccAddresses, bccAddresses = self.getEmailAddresses(emailConfig, emailContext)
					if addresses:
						subjectLine = emailConfig.get('subject','<no subject>')
						bodyTemplateName = emailConfig.get('bodyTemplateName','undefined')
						fullPathToTemplate = self.container.buildFullPathToSiteTemplate(site, bodyTemplateName)

						loader = envUtils.getEnvironment().getTemplateLoader()
						template = loader.load(fullPathToTemplate)
						body = template.generate(context=emailContext)

						emailDict = self.getEmailDict(addresses, ccAddresses, bccAddresses, subjectLine, body)
						self.persistAndSend(emailDict, doCommit)


	def wf_dependencySatisified(self,emailConfig):
		wfDependencyCode = emailConfig.get('workflow_dependency','')
		if not wfDependencyCode:
			return True
		jaSvc = jobActionSvc.JobActionService(self.connection)
		return jaSvc.isRubberBandedToJobActionOfType(self.jobActionDict.get('id',-1),wfDependencyCode)

	def prepareAndSendDirectiveEmailFromNonItem(self,emailConfig,fullPathToTemplate,personDict,doCommit=True):
		if emailConfig:
			site = self.profile.get('siteProfile',{}).get('site','')
			emailContext = self.initializeEmailContext()
			self.container.extendEmailContext(emailContext)

			addresses, ccAddresses, bccAddresses = self.getEmailAddresses(emailConfig, emailContext)
			if addresses:
				emailContext['url'] = self.getAlertUrl()
				emailContext['candidate'] = personDict
				subjectLine = emailConfig.get('subject','<no subject>')

				loader = envUtils.getEnvironment().getTemplateLoader()
				template = loader.load(fullPathToTemplate)
				body = template.generate(context=emailContext)

				emailDict = self.getEmailDict(addresses, ccAddresses, bccAddresses, subjectLine, body)
				self.persistAndSend(emailDict, doCommit)

	def resendEmail(self,emailId,recipient,doCommit = True):
		email = self.getEmail(emailId)
		emailDict = self.getResendEmailDict(recipient,email.get('email_subject',''),email.get('email_body',''),email.get('job_action_id',-1),email.get('task_code',''))
		self.persistAndSend(emailDict, doCommit)
		return 'ok'


	#   Solicitation emails.

	def prepareAndSendSolicitationEmail(self, _solicitationEmailContext, doCommit=True):
		addresses = self.stringifyAddressList(_solicitationEmailContext.get('addresses',[]))
		ccAddresses = self.stringifyAddressList(_solicitationEmailContext.get('ccAddresses',[]))
		bccAddresses = self.stringifyAddressList(_solicitationEmailContext.get('bccAddresses',[]))
		subjectLine = _solicitationEmailContext.get('subjectLine','')
		body = _solicitationEmailContext.get('body','')
		emailDict = self.getEmailDict(addresses, ccAddresses, bccAddresses, subjectLine, body)
		return self.persistAndSend(emailDict, doCommit)


	#   Common emailing tasks.

	def persistAndSend(self, _emailDict, doCommit):

		#   If an override EmailTo address is specified, use it.
		#
		#   An Override Email address can be specified at one of three levels: OS, Site, or Environment.
		#   An OS-level override takes priority over all others settings.
		#   Site is used as an override to explicitly direct email to a specific destination for specific Sites.
		#   The application Environment can also specify an override.
		#   Think of 'Environment' in this context as a server-wide setting.
		#
		#   In production environment, no overrides are usually specified. In all others, it is usually advantageous
		#   to specify some sort of override so that potential end-users of the system don't get bogus emails.
		#
		#   Look first for a OS-level setting. If the setting exists, we use it.
		#   Next look for a Site-level setting. If the setting exists in the given profile, we use it.
		#   The Site-level setting is used to explicitly direct all emails to a specific address for a specific Site.
		#   If no Site-level setting is specified, use any application Environment-specific setting.

		if os.environ.has_key('CAR_EMAILTO'):
			_emailDict['email_to'] = os.environ['CAR_EMAILTO']
			_emailDict['email_cc'] = ''
			_emailDict['email_bcc'] = ''
		else:
			sitePreferences = self.profile.get('siteProfile', {}).get('sitePreferences', {})
			if 'emailto' in sitePreferences:
				_emailDict['email_to'] = sitePreferences['emailto']
				_emailDict['email_cc'] = ''
				_emailDict['email_bcc'] = ''
			else:
				overrideTo = envUtils.getEnvironment().getEmailTo()
				if overrideTo:
					_emailDict['email_to'] = self.stringifyAddressList(overrideTo)
					_emailDict['email_cc'] = ''
					_emailDict['email_bcc'] = ''

		emSQL.createEMail(self.connection, _emailDict, doCommit)
		emailId = self.connection.getLastSequenceNbr('wf_email')
		email = emSQL.getMailById(self.connection, emailId)

		emailer = Emailer(email)
		result = emailer.sendMail()
		sent = (result == 'ok')
		emSQL.updateSentEmail(self.connection, emailId, result, sent, doCommit)
		return emailId

	def getEmailDict(self,addresses,ccAddresses,bccAddresses,subjectLine,body):
		emailDict = {}
		if self.jobActionDict:
			emailDict['job_action_id'] = self.jobActionDict.get('id',0)
		if self.jobTaskDict:
			emailDict['task_code'] = self.jobTaskDict.get('task_code', '')
		emailDict['email_from'] = kEmailFrom
		emailDict['email_to'] = addresses
		emailDict['email_cc'] = ccAddresses
		emailDict['email_bcc'] = bccAddresses
		emailDict['email_subject'] = subjectLine
		emailDict['email_body'] = body
		emailDict['email_date'] = self.now
		emailDict['email_sent'] = False
		emailDict['created'] = self.now
		emailDict['lastuser'] = self.username
		return emailDict

	def getResendEmailDict(self,addresses,subjectLine,body,jobActionId,taskCode):
		emailDict = {}
		emailDict['job_action_id'] = jobActionId
		emailDict['task_code'] = taskCode
		emailDict['email_from'] = kEmailFrom
		emailDict['email_to'] = addresses
		emailDict['email_cc'] = ''
		emailDict['email_bcc'] = ''
		emailDict['email_subject'] = subjectLine
		emailDict['email_body'] = body
		emailDict['email_date'] = self.now
		emailDict['email_sent'] = False
		emailDict['created'] = self.now
		emailDict['lastuser'] = self.username
		return emailDict


	def getEmailAddresses(self, _config, _emailContext):
		addresses = self.stringifyAddressList(_config.get('sendToAddresses',[]))
		ccAddresses = self.stringifyAddressList(_config.get('sendToBCCAddresses',[]))
		bccAddresses = self.stringifyAddressList(_config.get('sendToCCAddresses',[]))

		if _config.get('sendToCandidate', False):
			addresses += self.getCandidateEmailAddress()
		if _config.get('sendToUser', False):
			addresses += self.getUserEmailAddress()
		if _config.get('sendToDepartment', False):
			addresses += self.getDepartmentEmailAddress()
		if _config.get('sendToSitePref',[]):
			addresses += self.getSiteEmailAddresses(_config)

		containerSpecificAddressList = _emailContext.get('sendToAddresses',[])
		if containerSpecificAddressList:
			addresses += self.stringifyAddressList(containerSpecificAddressList)

		return addresses, ccAddresses, bccAddresses

	def stringifyAddressList(self,addressList):
		stringifiedValue = ""
		for emailaddress in addressList:
			stringifiedValue += self.delimitEmailAddress(emailaddress)
		return stringifiedValue

	def delimitEmailAddress(self,emailaddress):
		if emailaddress and not emailaddress.endswith(","):
			emailaddress += ","
		return emailaddress

	def getDepartmentEmailAddress(self):
		emailAddress = ''
		department = positionSvc.getDepartment(self.connection,self.jobActionDict.get('position_id',0))
		if department:
			emailAddress = self.stringifyAddressList([department.get('email_address','')])
		return emailAddress

	def getCandidateEmailAddress(self):
		emailAddress = ''
		person = personSvc.PersonService(self.connection).getPerson(self.jobActionDict.get('person_id',-1))
		if person:
			emailAddress = self.stringifyAddressList([person.get('email','')])
		return emailAddress

	def getUserEmailAddress(self):
		emailaddresses = ''
		userEmail = self.profile.get('userProfile',{}).get('userPreferences',{}).get('email','')
		if userEmail:
			emailaddresses += self.stringifyAddressList([userEmail])
		return emailaddresses

	def getSiteEmailAddresses(self,config):
		emailaddresses = ''
		for bigbrain in config.get('sendToSitePref',[]):
			emailaddresses += self.stringifyAddressList([self.profile.get('siteProfile',{}).get('sitePreferences',{}).get(bigbrain,'')])
		return emailaddresses

	def getEmailsForJobActionId(self):
		return emSQL.getEmailsForJobActionId(self.connection,self.jobActionDict.get('id',-1))

	def getEmail(self,emailId):
		return emSQL.getEmail(self.connection,emailId)

	def getBaseUrl(self, appCode='APPT'):
		siteAppList = self.profile.get('siteProfile',{}).get('siteApplications',{})
		for app in siteAppList:
			if app.get('code','') == appCode:
				return app.get('url','')
		return ''

	def initializeEmailContext(self):
		context = {}
		context['jobActionDict'] = self.jobActionDict
		context['jobTaskDict'] = self.jobTaskDict
		personDict = personSvc.PersonService(self.connection).getPerson(self.jobActionDict.get('person_id',-1))
		context['personDict'] = {} if not personDict else personDict
		context['profile'] = self.profile
		context['username'] = self.username
		context['now'] = self.now
		appList = self.profile.get('siteProfile',{}).get('siteApplications',[])
		appCode = envUtils.getEnvironment().getAppCode()
		candidateURL = "%s/mps/login/%s" % (coreEnvUtils.CoreEnvironment().getApplicationURLPrefix(appCode, appList), self.jobActionDict.get('external_key', ''))
		self.container.containerDict.get('config',{})['candidateurl'] = candidateURL
		context['container'] = self.container
		context['baseUrl'] = self.getBaseUrl()
		context['candidate_url'] = candidateURL
		return context

class Emailer:
	def __init__(self, _email):
		self.email = _email

	def formatEmailAddresses(self,addresses):
		parts = addresses.split(",")
		addressList = []
		for address in parts:
			addressList.append(address.strip())
		return COMMASPACE.join(addressList).strip()

	def sendMail(self,subtype = 'html'):
		message = 'ok'
		if envUtils.getEnvironment().getAvoidNetwork():
			return message

		try:
			fro = self.email.get('email_from','')
			to = self.formatEmailAddresses(self.email.get('email_to',''))
			msg = MIMEMultipart()
			msg['From'] = fro
			msg['To'] = to

			dst = []
			for addy in to.split(','):
				dst.append(addy.strip())

			cc = self.email.get('email_cc','')
			if cc:
				msg.add_header('Cc', cc)
				for addy in cc.split(','):
					dst.append(addy.strip())

			bcc = self.email.get('email_bcc','')
			if self.email.get('email_bcc',''):
				for addy in bcc.split(','):
					dst.append(addy.strip())

			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = str(self.email.get('email_subject',''))
			msg.attach(MIMEText(self.email.get('email_body',''), _subtype=subtype))
			for file in self.email.get('attachments',[]):
				#attachments are not currently being passed in. We'll need to figure out images, if and when, we need to
				#deal with them. The following code will attach the images to the mail. The 'content id' needs to be referenced
				#in the html <img src="cid:testimage"/> where testimage is the content id for the image. File name is probably
				#what we'll want to use.
				imgf = open(file,'rb')
				img = MIMEImage(imgf.read(), 'jpeg')
				imgf.close()
				img.add_header('Content-Id', '<testimage>')
				msg.attach(img)
			server = smtplib.SMTP('localhost')
			server.set_debuglevel(True)
			server.sendmail(fro, dst, msg.as_string())
			server.close()
		except Exception,e:
			message = str(e) + ' '
		finally:
			return message
