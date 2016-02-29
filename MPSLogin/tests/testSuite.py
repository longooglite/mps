# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import unittest
from MPSCore.tests.mpsTestCase import MPSTestSuite

class TestSuite(MPSTestSuite):
	def getTestSuite(self):
		testSuite = unittest.TestSuite()

		#testSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(testme.TestMe))

		return testSuite

