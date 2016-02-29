# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

config = {
	"reportName":"Evaluations Metrics",
	"srcFile":"evaluationsMetrics",
	"instructional":"Produces a series of metrics pertaining to the solicitation, reception and approval of external evaluations. <br/>Metrics will be calculated for job actions that were completed between start and end dates.",
	"itemCodes":['acad_eval'],
	"includeGraphs":True,
	"prompts": [
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