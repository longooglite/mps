# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

config = {
	"reportName":"Time to Completion",
	"srcFile":"timeToCompletion",
	"instructional":"Report to list average times for completed job actions that were started within specified time period.",
	"includeGraphs":True,
	"graphingJobActionTypes":["NEWAPPOINT","PROMOTION","CREDENTIAL","ENROLL"],

	"prompts": [
		{"affordancetype":"multipicklist",
		 "label":"Department",
		 "tableName":"wf_department",
		 "controlName":"department",
		 "restrictToUserPermission":True,
		 "required":True,
		 },
		{"affordancetype":"multipicklist",
		 "label":"Title",
		 "tableName":"wf_title",
		 "controlName":"title",
		 "restrictToUserPermission":False,
		 "required":True,
		 },
		{"affordancetype":"date_entry",
		 "label":"Start Date",
		 "controlName":"startDate",
		 "date_format":"MM/DD/YYYY",
		 "default":"minus_1_Y",
		 "validate_date_format":"Y/M/D",
		 "required":True,
		 },
		{"affordancetype":"date_entry",
		 "label":"End Date",
		 "controlName":"endDate",
		 "date_format":"MM/DD/YYYY",
		 "default":"now",
		 "validate_date_format":"Y/M/D",
		 "required":True,
		 },
	]
}