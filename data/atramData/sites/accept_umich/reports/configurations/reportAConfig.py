# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

config = {
	"reportName":"Report A",
	"srcFile":"reportA",
	"instructional":"Instructional text to splain stuff. Splain splain, splain splain splain splain, splain. Splain some more. All splained.",
	"orderBy":["something","something else"],
	"prompts": [
		{"affordancetype":"singlepicklist",
		 "label":"Department",
		 "tableName":"wf_department",
		 "controlName":"department",
		 "restrictToUserPermission":False,
		 "required":True,
		 },
		{"affordancetype":"multipicklist",
		 "label":"Title",
		 "tableName":"wf_title",
		 "controlName":"title",
		 "required":True,
		 },
		{"affordancetype":"date_entry",
		 "label":"Start Date",
		 "controlName":"startDate",
		 "date_format":"MM/DD/YYYY",
		 "validate_date_format":"Y/M/D",
		 "required":True,

		 },
		{"affordancetype":"date_entry",
		 "label":"End Date",
		 "controlName":"endDate",
		 "date_format":"MM/DD/YYYY",
		 "validate_date_format":"Y/M/D",
		 "required":True,
		 },
	]
}