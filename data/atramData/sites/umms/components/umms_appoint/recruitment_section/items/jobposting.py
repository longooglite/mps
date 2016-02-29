# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

jobposting = {
	"code": "jobposting",
	"comment":"",
	"descr": "Job Posting Information",
	"header": "Job Posting Information",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"overviewOnly":False,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ["approverfp"],
	"containers": [],
	"statusMsg": "Job Posted",
	"successMsg": "Job Posting saved",
	"className": "JobPosting",
	"config": {
		"alert": {
			"sendToUser":False,
			"sendToDepartment":True,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"emailTextComplete":"Job Posted",
		},
		"dashboardEvents": [{
			"code":"jopposted",
			"sortOrder":"b1",
			"eventDescription":"Job Posted",
			"eventType":"create",
			"permission":["dept_task"]
		},{
			"code":["rfpapproved","readyforjobposting"],
			"eventType":"remove",
		},],
		"waiverEnabled":True,
		"days":0,
		"postingTimeMetStatusMsg":"Posting Time Met",
		"postingWaivedStatusMsg":"Posting Was Waived",
		"waiverTasks":["rfp","approverfp"],
		"waiverCode":"JOB_POSTING_WAIVER",
		"waivedAffirmativeResponse":"Yes",
		"waiverUberQuestionCode": "RFP_Q00",
		"waiverUberAffirmativeResponse": "RFP_Q00_OPT_Y",

		"activityLog": {
			"enabled": True,
			"activityLogText": "Job Posting",
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
