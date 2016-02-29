# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

import os
from data.reporting.baseReport import BaseReport
import MPSAppt.core.constants as constants


class ReportA(BaseReport):
	def __init__(self, _parameters):
		BaseReport.__init__(self, _parameters)

	def run(self):
		connection = self.getConnection()
		try:
			corepath = os.path.abspath(__file__).split("car")[0] + "car" + os.sep
			sandboxPath = corepath + "misc" + os.sep + "sandbox" + os.sep
			if self.context.get('formData',{}).get('file_type','') == constants.kFileTypePDF:
				filePath = sandboxPath + "marina_packet.pdf"
			else:
				filePath = sandboxPath + "someTextFile.txt"

			self.persistReport(connection,filePath)
		finally:
			self.closeConnection()
