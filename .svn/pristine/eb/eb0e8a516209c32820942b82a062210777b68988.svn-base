# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import sys
import os
import os.path
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import optparse


import PIL
from PIL import Image
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
import MPSAppt.utilities.environmentUtils as envUtils
import shutil


#    was used for testing on CentOS servers. Do not need to keep this script around once we deploy code that scales images
#   and overlays to a pdf

class ImageHandling(object):
	def __init__(self, options=None, args=None):
		self.image = options.image
		self.pdf = options.pdf

	def process(self):
		scaledImagePath = self.scaleImage(100,self.image)
		print self.insertImageIntoPDF(scaledImagePath,self.pdf,[1],320,450)

	def scaleImage(self,basepixelwidth,srcImagePath):
		try:
			x=1/0
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
			print e
			pass

	def insertImageIntoPDF(self,insertImagePath,destPDFPath,pageNbrs,leftToRightCoord,bottomToTopCoord):
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
			print e
			pass
		finally:
			return finalOutputPath


class ImagineInterface:

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description='')
		parser.add_option('-i', '--sourceImage', dest='image', default='/tmp/dog.jpg', help='')
		parser.add_option('-p', '--destPDFPath', dest='pdf', default='/tmp/bellyflop.pdf', help='')

		return parser

	def run(self, options, args):
		try:
			imageHandler = ImageHandling(options, args)
			imageHandler.process()
		except Exception, e:
			print e

if __name__ == '__main__':
	interface = ImagineInterface()
	parser = interface.get_parser()
	(options, args) = parser.parse_args()
	interface.run(options, args)
	sys.exit(0)
