import PIL
from PIL import Image
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
import MPSAppt.utilities.environmentUtils as envUtils
import shutil
import fdfgen
import os


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
			input_page = input_file.getPage(page_number)
			#page_nbr is 0-based. Parameters are actual page numbers
			if page_number+1 in pageNbrs:
				# merge the watermark with the page
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


def autofillPDF(pdfPath,fields):
	env = envUtils.getEnvironment()
	fdf_data = fdfgen.forge_fdf("", fields, [], [], [])
	fdf_file_path = env.createGeneratedOutputFilePath('fdffile', '.fdf')
	fdf_file = open(fdf_file_path,"w")
	fdf_file.write(fdf_data)
	fdf_file.close()
	finalOutputPath = env.createGeneratedOutputFilePath('autofilled_', '.pdf')
	pdftk_cmd = "pdftk %s fill_form %s output %s " % (pdfPath,fdf_file_path,finalOutputPath)
	error = os.system(pdftk_cmd)
	return finalOutputPath

basewidth = 175
srcImagePath = '/Users/erpaul/Desktop/donald.jpg'
destImagePath = scaleImage(basewidth,srcImagePath)
destPDFPath = '/Users/erpaul/Desktop/PICA_form.pdf'

fields = [{'Applicant Name 1','Donald J Trump'},
          {'Applicant Name 2','Donald J Trump'},
          {'Applicant_Date','10-12-1999'},
          {'U of M Department Representative Name','Richard F Wadd'},
          {'UM_Date','10-12-1999'},
          {'foobarred','10-12-1999'},]
#'foobarred' field item - adding this attribute to fields list magically made the UM_Date autofill

autofilledPDFPath = autofillPDF(destPDFPath,fields)
imageInsertedPath = insertImageIntoPDF(destImagePath,autofilledPDFPath,pageNbrs=[1],leftToRightCoord=15,bottomToTopCoord=565)
