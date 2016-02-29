# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getTerminationTypes(_dbConnection):
	return _dbConnection.executeSQLQuery("SELECT * FROM wf_termination_type ORDER BY CODE",())