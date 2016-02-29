# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import unittest
import sys
import os
import os.path
import random
sys.path.append(os.path.abspath(__file__).split("CAR")[0] + "CAR" + os.sep)
import optparse


from MPSCV.tests.testSuite import TestSuite as cvTestSuite
from MPSCore.tests.testSuite import TestSuite as coreTestSuite
from MPSAdmin.tests.testSuite import TestSuite as adminTestSuite
from MPSAuthSvc.tests.testSuite import TestSuite as authTestSuite
from MPSLogin.tests.testSuite import TestSuite as loginTestSuite

OK = '\033[94m'
WARNING = '\033[91m'
ENDC = '\033[0m'


class Testifier(object):
	def __init__(self, options=None, args=None):
		self.options = options
		self.args = args

	def run(self):
		results = []
		results.append(self.runTestSuite(coreTestSuite(),"MPSCore",options.verbosity,options.package))
		results.append(self.runTestSuite(adminTestSuite(),"MPAdmin",options.verbosity,options.package))
		results.append(self.runTestSuite(authTestSuite(),"MPSAuthSvc",options.verbosity,options.package))
		results.append(self.runTestSuite(loginTestSuite(),"MPSLogin",options.verbosity,options.package))
		results.append(self.runTestSuite(cvTestSuite(),"MPSCV",options.verbosity,options.package))
		self.displaySynopsis(results)

	def runTestSuite(self, theSuite, descr, verbosity, package):
		if package == '' or package == descr:
			suite = theSuite.getTestSuite()
			return unittest.TextTestRunner(verbosity=verbosity).run(suite)
		return None

	def displaySynopsis(self,results):
		testsRun = 0
		failures = 0
		for each in results:
			if each <> None:
				testsRun += each.testsRun
				failures += len(each.failures)
		print ""
		if failures == 0:
			print OK + "Tests run: %i, Failures: %i" % (testsRun,failures) + ENDC
		else:
			print WARNING + "Tests run: %i, Failures: %i" % (testsRun,failures) + ENDC
		print ""
		if failures == 0:
			print OK + "SUCCESS" + ENDC
		else:
			print WARNING + self.getFailureReason() + ENDC
		print ""


	def getFailureReason(self):
		failures = []
		failures.append("It's probably best that you don't check in")
		failures.append("Hey Doof, the tests are broken.")
		failures.append("Whoopsy Daisy.")
		failures.append("Kablammo!")
		failures.append("Fail.")
		failures.append("Tests Failed. Try commenting them out.")

		return failures[random.randrange(0,len(failures))]


class TestifierItemServiceImpl:
	def run(self, options, args):
		try:
			testifier = Testifier(options, args)
			testifier.run()
		except Exception, e:
			print e.originalMessage
			for each in e.stack:
				print each
		finally:
			pass

	def get_parser(self):
		parser = optparse.OptionParser(description="Unit tests")
		parser.add_option('-p', '--package', dest='package', default='', help='run one package, values = MPSCore, MPSLogin, MPSAuthSvc, MPSCV, MPSLogin')
		parser.add_option('-v', '--verbosity', dest='verbosity', default=2, help='verbosity')
		return parser


if __name__ == '__main__':
	testifierItemServiceImpl = TestifierItemServiceImpl()
	parser = testifierItemServiceImpl.get_parser()
	(options, args) = parser.parse_args()
	testifierItemServiceImpl.run(options, args)



