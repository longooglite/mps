from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

packet = StringIO.StringIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(500, 10, "some new string")
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(file("/Users/erpaul/Desktop/ummsnpiform.pdf", "rb"))
pages = existing_pdf.getNumPages()
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
page = existing_pdf.getPage(1)
output.addPage(page)
page = existing_pdf.getPage(2)
output.addPage(page)

# finally, write "output" to a real file
outputStream = file("/Users/erpaul/Desktop/ummsnpiform2.pdf", "wb")
output.write(outputStream)
outputStream.close()