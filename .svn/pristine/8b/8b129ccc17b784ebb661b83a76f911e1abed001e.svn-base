# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

job_posting_info = {
	"code": "job_posting_info",
	"comment":"",
	"descr": '''Job Posting Information''',
	"header": '''Job Posting Information''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task","ofa_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Job Posting Information Complete",
	"className": "JobPosting",
	"config": {
		"waiverEnabled":True,
		"days":7,
		"postingTimeMetStatusMsg":"Posting Time Met",
		"postingWaivedStatusMsg":"Posting Was Waived",

		"activityLog": {
			"enabled": True,
			"activityLogText": "Job Posting Information",
		},
		"prompts": [
			{
				"code": "posting_number",
				"label": "Job Posting #",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "date_posted",
				"label": "Date Posted",
				"enabled": True,
				"required": True,
				"data_type": "date",
				"date_format":"M/D/Y"
			},
		]
	},
}
