# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import datetime
import os
import shutil
import subprocess
from PyPDF2 import PdfFileMerger
import MPSAppt.utilities.environmentUtils as envUtils
import fdfgen
from PyPDF2 import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import PIL
from PIL import Image

#   take html and create pdf with optional footer
def createPDFFromHTML(html, env, name = "", setFooter = True, prefix = 'cv_',portrait = True, includeFooterTime=True):
	pdfFilePath = env.createGeneratedOutputFilePath(prefix, '.pdf')
	htmlFilePath = env.createGeneratedOutputFilePath(prefix, '.html')
	wkhtmltopdfBinaryPath = env.getWkhtmltopdfBinPath()

	f = None
	try:
		f = open(htmlFilePath, 'w')
		f.write(html)
		f.flush()
	finally:
		if f:
			try: f.close()
			except Exception, e: pass

	args = []
	args.append(wkhtmltopdfBinaryPath)
	if setFooter:
		args.append("--footer-left")
		args.append(name)
		args.append("--footer-center")
		if includeFooterTime:
			args.append(datetime.datetime.now().strftime("%b %d, %Y %I:%M %p"))
		else:
			args.append(datetime.datetime.now().strftime("%b %d, %Y"))
		args.append("--footer-right")
		args.append("Page [page] of [topage]")
		args.append("--footer-font-size")
		args.append("9")
		if not portrait:
			args.append("--orientation")
			args.append("landscape")

	args.append(htmlFilePath)
	args.append(pdfFilePath)
	subprocess.check_call(args)

	try: os.remove(htmlFilePath)
	except Exception, e: pass

	return env.getUxGeneratedOutputFilePath(pdfFilePath),pdfFilePath

#   get page count and write to standard format we know we can read before uploading
def getPageCountAndNormalizePDFContent(fullpath):
	existingPDF = PdfFileReader(open(fullpath,'rb'))
	pages = existingPDF.getNumPages()
	output = PdfFileWriter()
	i = 0
	while i < pages:
		output.addPage(existingPDF.getPage(i))
		i+=1
	os.remove(fullpath)
	outputStream = file(fullpath, "wb")
	output.write(outputStream)
	outputStream.close()
	return pages

def getPDFVersion(content):
	version = ''
	try:
		version = content[1:8].strip()
	except Exception,e:
		pass
	return version

#   take a bunch of pdfs and create a packet u pdfs
def mergePDFsToOne(pdfList):
	env = envUtils.getEnvironment()
	merger = PdfFileMerger()
	content = None
	if pdfList:
		for pdf in pdfList:
			pdfPath = env.createGeneratedOutputFilePath('file_', '.pdf')
			f = open(pdfPath,'wb')
			f.write(bytearray(pdf.get('content','')))
			f.flush()
			f.close()
			merger.append(open(pdfPath),pdfPath)
		mergedPacketPath = env.createGeneratedOutputFilePath('merged_', '.pdf')
		output = open(mergedPacketPath, "wb")
		merger.write(output)
		output.flush()
		output.close()
		merger.close()
		f = open(mergedPacketPath,'rb')
		content = bytearray(f.read())
		f.close()
		pages = getPageCountAndNormalizePDFContent(mergedPacketPath)
	else:
		pages = 0
	return content,pages

#   autofill pdf

def autofillPDF(pdfPath,fields):
	env = envUtils.getEnvironment()
	formout = env.createGeneratedOutputFilePath('file_', '.pdf')
	try:
		pdftkBinaryPath = env.getPDFtkBinPath()
		fdf_data = fdfgen.forge_fdf("", fields, [], [], [])
		fdf_file_path = env.createGeneratedOutputFilePath('file_', '.fdf')
		fdf_file = open(fdf_file_path,"w")
		fdf_file.write(fdf_data)
		fdf_file.close()
		pdftk_cmd = "%s %s fill_form %s output %s" % (pdftkBinaryPath,pdfPath,fdf_file_path,formout)
		error = os.system(pdftk_cmd)
		if error <> 0:
			formout = pdfPath
	except Exception,e:
		#if the form won't autofill, eat the error and return the original form
		formout = pdfPath
		pass
	return formout

#   footer

def appendToPDFFooter(path,footerString,pages):
	env = envUtils.getEnvironment()
	packet = StringIO.StringIO()
	# create a new PDF with Reportlab
	can = canvas.Canvas(packet, pagesize=letter)
	can.drawString(400, 10, footerString)
	can.save()
	destPath = "%s%s%s%s%s" % (os.sep,"tmp",os.sep,"pdf",os.sep)

	#move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)
	# read existing PDF
	existing_pdf = PdfFileReader(file(path, "rb"))
	totalPages = existing_pdf.getNumPages()
	i=0
	modFileName = ''
	if totalPages > 0:
		output = PdfFileWriter()
		page = existing_pdf.getPage(0)
		if (i+1) in pages:
			page.mergePage(new_pdf.getPage(0))

		output.addPage(page)
		i = 1
		while i < totalPages:
			page = existing_pdf.getPage(i)
			if (i+1) in pages:
				page.mergePage(new_pdf.getPage(0))
			output.addPage(page)
			i += 1

		# finally, write out new file
		modFileName = env.generateUniqueId() + '.pdf'
		outputStream = file(destPath + modFileName, "wb")
		output.write(outputStream)
		outputStream.close()

	return modFileName

#   image scaling and overlay

def scaleImage(basepixelwidth,srcImagePath):
	try:
		env = envUtils.getEnvironment()
		#take an image, and scale it, while maintaining aspect ratio, and maximizing image size
		finalOutputPath = env.createGeneratedOutputFilePath('scaled_', '.png')
		#make copy of file to not destroy original
		shutil.copyfile(srcImagePath,finalOutputPath)
		img = Image.open(finalOutputPath)
		#determine scaling percentage
		wpercent = (basepixelwidth/float(img.size[0]))
		if img.size[0] >= img.size[1]:
			size = int((float(img.size[1])*float(wpercent)))
		else:
			size = int((float(img.size[0])*float(wpercent)))
		#resize image and save
		img = img.resize((basepixelwidth,size), PIL.Image.ANTIALIAS)
		img.save(finalOutputPath)
		return finalOutputPath
	except Exception, e:
		pass

def insertImageIntoPDF(insertImagePath,destPDFPath,pageNbrs,leftToRightCoord,bottomToTopCoord):
	env = envUtils.getEnvironment()
	finalOutputPath = None
	try:
		# if we want the image on all pages, pass an empty pageNbrs array, else pass specific page numbers
		# Create an overlay pdf
		overlayPath = env.createGeneratedOutputFilePath('overlay_', '.pdf')
		c = canvas.Canvas(overlayPath)

		# Draw the image at a the position it needs to be placed in the final output
		c.drawImage(insertImagePath, leftToRightCoord, bottomToTopCoord)
		# Save the overlay
		c.save()

		# Get the overlay file we just created
		watermark = PdfFileReader(open(overlayPath, "rb"))

		# open the target pdf
		output_file = PdfFileWriter()
		input_file = PdfFileReader(open(destPDFPath, "rb"))

		# Number of pages in input document
		page_count = input_file.getNumPages()

		# Go through all the input file pages and add overlay to target pdf
		for page_number in range(page_count):
			#page_nbr is 0-based. Parameters are actual page numbers
			if not pageNbrs or page_number+1 in pageNbrs:
				# merge the watermark with the page
				input_page = input_file.getPage(page_number)
				input_page.mergePage(watermark.getPage(0))
				# add page from input file to output document
				output_file.addPage(input_page)

		# finally, write to a 3rd, final, output pdf with original content and overlay merged
		finalOutputPath = env.createGeneratedOutputFilePath('img_merge_', '.pdf')
		with open(finalOutputPath, "wb") as outputStream:
			output_file.write(outputStream)
	except Exception, e:
		pass
	finally:
		return finalOutputPath
