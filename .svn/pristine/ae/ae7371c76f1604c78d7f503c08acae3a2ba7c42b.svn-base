__author__ = 'erpaul'

import fdfgen
import os

npiform ='/Users/erpaul/Desktop/ummsnpiform.pdf'
npiformout ='/Users/erpaul/Desktop/ummsnpiformfilled.pdf'

fields = [{'2 First_2','Bartholomew'},
          {'3 Middle_2','J.'},
          {'4 Last_2',u'Morinski'},
          {'7 TitlePosition_2',u'King of Credentialing'},
          {'8 EMail Address',u'Bart@Morinski.com'},
          {'9 Telephone Number Include Area Code',u'734-936-2047'}]

fdf_data = fdfgen.forge_fdf("", fields, [], [], [])
fdf_file_path = "/Users/erpaul/Desktop/file_fdf.fdf"
fdf_file = open(fdf_file_path,"w")
fdf_file.write(fdf_data)
fdf_file.close()

#Run pdftk system command to populate the pdf file. The file "file_fdf.fdf" is pushed in to "input_pdf.pdf" thats generated as a new "output_pdf.pdf" file.
pdftk_cmd = "pdftk %s fill_form %s output %s " % (npiform,fdf_file_path,npiformout)
os.system(pdftk_cmd)