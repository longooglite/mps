# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import MPSCore.utilities.PDFUtils as pdfUtils
import MPSCore.utilities.stringUtilities as stringUtils


def getExternalReviewersList(evaluatorsReceived,evaluatorsDeclined,evaluatorTypeDict,evalSourceDict,env):
	content = None
	pages = 0
	refusedContent = None
	receivedContent = None
	if evaluatorsReceived:
		title = "ALPHABETICAL LISTING OF EXTERNAL REVIEWERS WHO PROVIDED LETTERS"
		receivedHTML = buildBioPage(evaluatorsReceived,evaluatorTypeDict,evalSourceDict,title)
		receivedPDF = pdfUtils.createPDFFromHTML(receivedHTML,env,"",False,"eval_")
		f = open(receivedPDF[1],'rb')
		receivedContent = bytearray(f.read())
		f.close()
	if evaluatorsDeclined:
		title = "ALPHABETICAL LISTING OF EXTERNAL REVIEWERS FROM WHOM LETTERS WERE REQUESTED BUT WHO DECLINED AND THE REASONS FOR DECLINING"
		refusedHTML = buildBioPage(evaluatorsDeclined,evaluatorTypeDict,evalSourceDict,title)
		refusedPDF = pdfUtils.createPDFFromHTML(refusedHTML,env,"",False,"eval_")
		f = open(refusedPDF[1],'rb')
		refusedContent = bytearray(f.read())
		f.close()

	if refusedContent and receivedContent:
		content,pages = pdfUtils.mergePDFsToOne([{"content":receivedContent},{"content":refusedContent}])
	elif receivedContent:
		content,pages = pdfUtils.mergePDFsToOne([{"content":receivedContent}])
	elif refusedContent:
		content,pages = pdfUtils.mergePDFsToOne([{"content":refusedContent}])

	return content,pages


def buildBioPage(evaluatorsList,evaluatorTypeDict,evalSourceDict,title,declination = False):
	header = getBioHeader()
	title = "<center><b>%s</b></center><br/><br/>" % (title)
	body = ''
	for evaluator in evaluatorsList:
		body += getBioBody(evaluator,evaluatorTypeDict,evalSourceDict,declination)
		body += "<br/><br/>"
	footer = getBioFooter()
	return header + title + body + footer

def getBio(evaluator,evaluatorTypeDict,evalSourceDict,_env):
	header = getBioHeader()
	body = getBioBody(evaluator,evaluatorTypeDict,evalSourceDict)
	footer = getBioFooter()
	bio_pdf = pdfUtils.createPDFFromHTML(header+body+footer, _env, name = "", setFooter = False, prefix = 'eval_')
	f = open(bio_pdf[1],'rb')
	content = bytearray(f.read())
	f.close()
	return {"content":content}

def getBioBody(evaluator,evaluatorTypeDict,evalSourceDict,declination = False):
	name = stringUtils.constructFullName(evaluator.get('first_name',''),evaluator.get('middle_name',''),evaluator.get('last_name',''))
	if evaluator.get('degree',''):
		name += ", %s" % (evaluator.get('degree',''))
	name += ' - '
	titleString = ''
	for title in evaluator.get('titles',[]):
		titleString = title.strip() + ' and '
	if titleString:
		titleString = titleString[0:len(titleString) - 5]
	if evaluator.get('institution',''):
		titleString += ', %s.' % (evaluator.get('institution',''))
	else:
		titleString += '.'
	if declination:
		reason = evaluator.get('reason','') + ' - '
	else:
		reason = evaluator.get('declined_comment','') + ' - '
	evaluatorType = evaluatorTypeDict.get(evaluator.get('evaluator_type_id',-1))
	armsLengthDescription = ''
	if evaluatorType:
		if evaluatorType.get('is_arms_length',False):
			armsLengthDescription = "Arm's Length"
		else:
			armsLengthDescription = "Not Arm's Length"
	evaluatorSource = evalSourceDict.get(evaluator.get('evaluator_source_id',{})).get('descr','')
	evaluatorSourceDescr = evaluatorSource = "suggested by %s" % (evaluatorSource)
	return "<b>%s</b>%s %s<b>%s, %s</b>" % (name,titleString,reason,armsLengthDescription,evaluatorSourceDescr)

def getBioHeader():
	return "<html><body>"

def getBioFooter():
	return "</body></html>"

