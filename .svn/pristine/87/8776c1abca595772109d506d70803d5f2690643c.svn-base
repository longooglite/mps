import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email.mime.image import MIMEImage


class Emailer:
	def __init__(self,_email):
		self.email = _email

	def formatEmailAddresses(self,addresses):
		parts = addresses.split(",")
		addressList = []
		for address in parts:
			addressList.append(address.strip())
		return COMMASPACE.join(addressList).strip()

	def sendMail(self):
		message = 'ok'
		try:
			fro = self.email.get('email_from','')
			to = self.formatEmailAddresses(self.email.get('email_to',''))
			msg = MIMEMultipart()
			msg['From'] = fro
			msg['To'] = to

			to = [to]
			cc = self.email.get('email_cc','')
			if cc:
				msg.add_header('Cc', cc)
				cc = [cc]
				to += cc

			bcc = self.email.get('email_bcc','')
			if self.email.get('email_bcc',''):
				bcc = [bcc]
				to += bcc

			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = str(self.email.get('email_subject',''))
			msg.attach(MIMEText(self.email.get('email_body',''), _subtype='html'))
			for file in self.email.get('attachments',[]):
				#attachments are not currently being passed in. We'll need to figure out images, if and when, we need to
				#deal with them. The following code will attach the images to the mail. The 'content id' needs to be referenced
				#in the html <img src="cid:testimage"/> where testimage is the content id for the image. File name is probably
				#what we'll want to use.
				imgf = open(file,'rb')
				img = MIMEImage(imgf.read(), 'jpeg')
				imgf.close()
				img.add_header('Content-Id', '<testimage>')
				msg.attach(img)
			server = smtplib.SMTP('localhost')
			server.set_debuglevel(True)
			server.sendmail(fro, to, msg.as_string() )
			server.close()
		except Exception,e:
			message = str(e) + ' '
			print message
		finally:
			return message

if __name__ == '__main__':
	emailDict = {}
	emailDict["email_to"] = 'eric <eric.paul@mountainpasssolutions.com>'
	emailDict["email_from"] = 'smartpath@mtnpass.com'
	emailDict["email_bcc"] = 'greg.poth@mountainpasssolutions.com'
	emailDict["email_subject"] = 'sum subject'
	emailDict["email_body"] = "Hello!, Heya buddy! Say hello to Python! :)"

	emailer = Emailer(emailDict)
	emailer.sendMail()