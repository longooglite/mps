# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import sys
import os
import os.path
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)

import csv
import optparse

class LDAPLoad(object):
	def __init__(self, options=None, args=None):
		pass

	def shutdown(self):
		pass

	def process(self):
		srcFilename = 'personconfig.txt'
		srcFilepath = os.path.join(os.path.abspath(__file__).split("car")[0], 'car', 'config', 'devserver', srcFilename)
		print "Src: %s" % (srcFilepath,)
		dstFilename = 'personconfig.ldif'
		dstFilepath = os.path.join(os.path.abspath(__file__).split("car")[0], 'car', 'config', 'devserver', dstFilename)
		print "Dst: %s" % (dstFilepath,)

		f = open(srcFilepath, 'rU')
		data = list(csv.reader(f, delimiter='|'))
		f.close()

		import pprint

		f = open(dstFilepath, 'w')
		for row in data:
			self.processRow(row, f)
		f.close()

	def processRow(self, _row, _dstfile):
		if len(_row) >= 7:
			username = _row[0].strip()
			password = _row[1].strip()
			encrypted = _row[2].strip()
			firstName = _row[3].strip()
			lastName = _row[4].strip()
			fullName = _row[5].strip()
			email = _row[6].strip()

			if not username.startswith('#'):
				if not fullName:
					fullName = ("%s %s" % (firstName, lastName)).strip()

				_dstfile.write('''dn: uid=%s,ou=users,dc=mntnpass,dc=com\n''' % (username,))
				_dstfile.write('''changetype: delete\n''')
				_dstfile.write('''\n''')

				_dstfile.write('''dn: uid=%s,ou=users,dc=mntnpass,dc=com\n''' % (username,))
				_dstfile.write('''cn: %s\n''' % (fullName,))
				_dstfile.write('''sn: %s\n''' % (lastName,))
				if firstName:
					_dstfile.write('''gn: %s\n''' % (firstName,))
				_dstfile.write('''objectClass: person\n''')
				_dstfile.write('''objectClass: inetOrgPerson\n''')
				if email:
					_dstfile.write('''mail: %s\n''' % (email,))
				_dstfile.write('''# password: %s\n''' % (password,))
				_dstfile.write('''userPassword: %s\n''' % (encrypted,))
				_dstfile.write('''\n''')


class LoadInterface:
	DESCR = '''Convert LDAP pipe-delimited text file to LDIF format'''

	def __init__(self):
		pass

	def get_parser(self):
		parser = optparse.OptionParser(description=self.DESCR)
		return parser

	def run(self, options, args):
		ldapLoad = None
		try:
			ldapLoad = LDAPLoad(options, args)
			ldapLoad.process()
		except Exception, e:
			print e.message
		finally:
			if ldapLoad:
				ldapLoad.shutdown()

if __name__ == '__main__':
	loadInterface = LoadInterface()
	parser = loadInterface.get_parser()
	(options, args) = parser.parse_args()
	loadInterface.run(options, args)
