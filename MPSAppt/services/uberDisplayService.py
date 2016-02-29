# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

from MPSAppt.services.abstractTaskService import AbstractTaskService
import MPSAppt.services.uberResolverService as uberResolverService
import MPSAppt.services.uberService as uberSvc
import MPSCore.utilities.PDFUtils as pdfUtils

class UberDisplayService(AbstractTaskService):
	def __init__(self, _connection,_doNotMaskCodes = None):
		AbstractTaskService.__init__(self, _connection)
		self.doNotMaskCodes = _doNotMaskCodes

	def getPacketContent(self,_workflow,_templateLoader,_task_code,_environment,_context):
		container = _workflow.getContainer(_task_code)
		context = {}
		context['uberContent'] = self.getContent(container,_context.get('siteProfile',{}).get('sitePreferences',{}))
		context['header'] = container.containerDict.get('header','')
		context['candidateName'] = _context.get('candidate_name','')
		context.update(container.getEditContext({}))

		template = _templateLoader.load('uberPrint.html')
		html = template.generate(context=context)
		content = None
		f = None
		fullPath = ''
		pages = 0
		try:
			pdf, fullPath = pdfUtils.createPDFFromHTML(html, _environment,name=container.getDescr(), setFooter=True, prefix = 'uberOut_')
			pages = pdfUtils.getPageCountAndNormalizePDFContent(fullPath)
			f = open(fullPath,'rb')
			content = bytearray(f.read())
		except:
			pass
		finally:
			if f:
				f.close()
			return {"descr":fullPath,"content":content,"pages":pages}

	def getContent(self, _container, _sitePreferences):
		groups = []
		resolverService = uberResolverService.UberResolverService(self.connection, _sitePreferences,self.doNotMaskCodes)

		allSections = _container.getEditContext(_sitePreferences,self.doNotMaskCodes).get('uber_instance', {}).get('questions', {}).get('elements', [])
		lastGroupDescr = ''
		lastGroupCode = ''
		isGrouped = False
		group = {'groupdescr':lastGroupDescr,"items":[]}

		for section in allSections:
			groupDescr = self.getGroupDescription(section)
			groupCode = section.get('code','')
			if groupCode <> lastGroupCode:
				group = {'code':groupCode,'groupdescr':groupDescr,"items":[]}
				isGrouped = True

			if section.get('repeating', False):
				for idx in range(0, section.get('response_count', 0)):
					resolvedSection = resolverService.resolveQuestionsInRepeatingGroup(section, idx)
					group['items'].extend(resolvedSection)
					if resolvedSection:
						group['items'].append(self._blankItem())
				if isGrouped:
					groups.append(group)
			else:
				resolvedSection = resolverService.resolveQuestionsInGroup(section)
				group['items'].extend(resolvedSection)
				if isGrouped:
					groups.append(group)

		if not isGrouped:
			groups.append(group)
		return groups

	def getGroupDescription(self,section):
		descr = ''
		if section.get('type','') == uberSvc.kElementTypeGroup:
			if section.get('display_text',''):
				descr = section.get('display_text','')
			else:
				for el in section.get('elements',[]):
					if el.get('type','') == uberSvc.kElementTypeGroup:
						if el.get('display_text',''):
							descr = el.get('display_text','')
							break
		return descr

	def _blankItem(self):
		return { 'label': '<br/>', 'value': '' }

