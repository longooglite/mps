# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os

from MPSAppt.modules.abstractArtifact import AbstractArtifact
import MPSAppt.utilities.environmentUtils as envUtils
import MPSCore.utilities.PDFUtils as pdfUtils

class Artifact(AbstractArtifact):
	def __init__(self, params):
		AbstractArtifact.__init__(self, params)

	def getContent(self):
		f = None
		try:
			config = eval(self.config)
			html = '''<html><body>PLACEHOLDER<div class="clear"><div class="clear">%s<div class="clear"><div class="clear"></div>%s</body></html>''' % (config.get('placeholder_descr','placeholder'),config.get('placeholder_notes',''))
			pdffilename,pdffullPath = pdfUtils.createPDFFromHTML(html, self.env,"",False,'ari_')
			f = open(pdffullPath,'rb')
			content = bytearray(f.read())
			f.close()
			return {"descr":config.get('placeholder_descr'),"content":content,"pages":1}
		except Exception,e:
			pass

