# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

config = {
	"reportName":"Actions in Progress",
	"srcFile":"actionsInProgress",
	"instructional":"Report to list job action currently in progress.",
	"includeGraphs":True,
	"graphingJobActionTypes":["NEWAPPOINT","PROMOTION"],
	"prompts": [
		{"affordancetype":"multipicklist",
		 "label":"Department",
		 "tableName":"wf_department",
		 "controlName":"department",
		 "restrictToUserPermission":True,
		 "required":True,
		 },
	]
}