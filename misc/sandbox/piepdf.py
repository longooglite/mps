from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
from PyPDF2.pdf import RectangleObject
from weasyprint import HTML
import os
import subprocess


import os

packetPath = '/packets/'

merger = PdfFileMerger()

dir = os.listdir(packetPath)

pages = []
for sumpacket in dir:
	if not sumpacket.startswith('.'):
		pdf = PdfFileReader(open(packetPath + sumpacket,'rb'))
		numPages = pdf.getNumPages()
		pages.append({'title':sumpacket,'pages': numPages})

		merger.append(open(packetPath + sumpacket),sumpacket)

output = open(os.path.expanduser("~/Desktop/moiged.pdf"), "wb")
merger.write(output)
output.close()
merger.close()


try:
	src_file = os.path.expanduser("~/Desktop/moiged.pdf")
	reader=PdfFileReader(open(src_file))
	output = PdfFileWriter()
	numPages = reader.getNumPages()
	i = 0
	while i < numPages:
		output.addPage(reader.getPage(i))
		i = i + 1


	#wkhtmltopdf --footer-right "Page [page] of [topage]" --footer-center "Oct 21, 2013" --footer-left "Kevin Chi Chung" /Users/erpaul/Desktop/test.html /Users/erpaul/Desktop/test.pdf

	#wheezieprint sucks use wkhtmltopdf
	####HTML('toc.html').write_pdf(os.path.expanduser(os.path.expanduser("~/Desktop/toc.pdf")))
	tocPath = os.path.expanduser("~/Desktop/toc.pdf")
	subprocess.check_call(["wkhtmltopdf", "toc.html", tocPath])

	toc = PdfFileReader(open(os.path.expanduser("~/Desktop/toc.pdf")))
	output.insertPage(toc.getPage(0),0)
	path = os.path.expanduser("~/Desktop/moigedwithtoc.pdf")
	outputStream = file(path, "wb")
	output.write(outputStream)
	outputStream.close()


except Exception,e:
	pass

########################## install #####################

''' pip install and easy_install did not work for me for PyPDF2.
The files downloaded, the code compiled without error and the egg was and installed into site_packages.
However, it would not import into python.


this worked...
download from https://pypi.python.org/pypi/PyPDF2/1.24

python setup.py build
python setup.py install
sudo python setup.py install

wkhtmltopdf - binaries located at

http://wkhtmltopdf.org/downloads.html

'''
