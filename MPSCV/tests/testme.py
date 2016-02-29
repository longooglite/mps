# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import unittest
from MPSCore.tests.mpsTestCase import MPSTestCase

class TestMe(MPSTestCase):
	def testDatGergsADoofus(self):
		self.assertEqual('GergisdADoofus','GergisdADoofus',"Yup, He's A Doof")

class TestMe2(MPSTestCase):
	def testDatGergsADoofie(self):
		self.assertEqual('GergisdADoofie','GergisdADoofie',"Yup, He's A Doofie too")

