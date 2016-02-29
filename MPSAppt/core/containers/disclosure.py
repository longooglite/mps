# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.core.containers.task import Task
import MPSAppt.services.disclosureService as disclosureSvc

class Disclosure(Task):
	def __init__(self, containerCode, parameterBlock):
		Task.__init__(self, containerCode, parameterBlock)
		self.setDisclosure({})


	#   Getters/Setters.

	def getDisclosure(self): return self.disclosureDict
	def setDisclosure(self, _disclosureDict): self.disclosureDict = _disclosureDict

	#   Data loading.

	def loadInstance(self):
		if self.getIsLoaded():
			return

		self.setIsLoaded(True)
		if not self.getIsEnabled():
			return

		jobTask = self.getPrimaryJobTaskDict()
		if jobTask:
			resultDict = disclosureSvc.DisclosureService(self.getWorkflow().getConnection()).getFullDisclosure(jobTask.get('id',0))
			if resultDict:
				self.setDisclosure(resultDict)


	#   Everything else.

	def getDataDict(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			dataDict = {}
			dataDict['url'] = self._getURL()
			dataDict['disabled'] = self.standardTaskDisabledCheck()
			return dataDict

		return {}

	def getEditContext(self, _sitePreferences):
		self.loadInstance()
		if self.getIsEnabled():
			context = self.getCommonEditContext(_sitePreferences)
			context['url'] = self._getURL()
			context['button_text'] = 'Submit'
			context['button_url'] = self._getURL()

			context['disclosure'] = {}
			context['is_crook'] = False
			context['not_crook'] = True
			disclosure = self.getDisclosure()
			if disclosure:
				context['disclosure'] = disclosure
				context['is_crook'] = disclosure.get('has_disclosures', False)
				context['not_crook'] = not context['is_crook']
				self.prepDisclosureForDisplay(disclosure, _sitePreferences)

			context['prompts'] = self.getConfigDict().get('prompts',[])
			context['offenses'] = disclosure.get('offenses', [])

			#   Create one empty Offense block if no entered Offenses
			if not context['offenses']:
				context['offenses'].append(self.createEmptyOffense())

			site = _sitePreferences.get('code','')
			templateName = self.getConfigDict().get('templateName','undefined')
			context['templateName'] = self.buildFullPathToSiteTemplate(site, templateName)

			return context

		return {}

	def prepDisclosureForDisplay(self, _disclosure, _sitePreferences):

		#   Localize dates/timestamps
		#   Assign each prompt field a unique value to be used as its UX 'name' field value

		if _disclosure:
			timezone = _sitePreferences.get('timezone', 'US/Eastern')
			format = _sitePreferences.get('ymdhmformat', '%m/%d/%Y %H:%M')
			_disclosure['created'] = self.localizeDate(_disclosure.get('created',''), timezone, format)
			_disclosure['updated'] = self.localizeDate(_disclosure.get('updated',''), timezone, format)
			for offenseAggregate in _disclosure.get('offenses', []):
				offenseNbr = int(offenseAggregate.get('offense_nbr','0'))
				offenseAggregate['fields'] = {}
				for fieldDict in offenseAggregate.get('field_list', []):
					code = fieldDict.get('offense_key','')
					fieldDict['created'] = self.localizeDate(fieldDict.get('created',''), timezone, format)
					fieldDict['updated'] = self.localizeDate(fieldDict.get('updated',''), timezone, format)
					fieldDict['ux_key'] = self.createOffenseFieldKey(fieldDict, offenseNbr)
					offenseAggregate['fields'][code] = fieldDict

	def createEmptyOffense(self, _offenseNbr=1):
		mtOffense = {}
		mtOffense['offense_nbr'] = _offenseNbr
		mtOffense['fields'] = {}
		for each in self.getConfigDict().get('prompts',[]):
			if each.get('enabled', False):
				code = each.get('code','')
				fieldDict = {}
				fieldDict['offense_nbr'] = _offenseNbr
				fieldDict['offense_key'] = code
				fieldDict['offense_value'] = ''
				fieldDict['ux_key'] = self.createOffenseFieldKey(fieldDict, _offenseNbr)
				mtOffense['fields'][code] = fieldDict
		return mtOffense

	def createOffenseFieldKey(self, _fieldDict, _offenseNbr):
		return "%s_%s" % (_fieldDict.get('offense_key',''), str(_offenseNbr))

	def _getURL(self, _prefix='/appt/jobaction/disclosure'):
		jobActionIdStr = str(self.getWorkflow().getJobActionDict().get('id',0))
		return '%s/%s/%s' % (_prefix, jobActionIdStr, self.getCode())

	def isComplete(self):
		self.loadInstance()
		if self.getIsEnabled():
			if self.getDisclosure():
				return True

			return False
		return True
