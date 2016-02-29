# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

identifycandidate = {
	"code": "identifycandidate",
	"descr": "Identify Candidate",
	"header": "Identify Candidate",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly": False,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task","ofa_task","mss_task"],
	"blockers": ["jobposting"],
	"statusMsg": "Candidate Identified",
	"successMsg":"Candidate information saved",
	"className": "IdentifyCandidate",
	"config": {
		"dashboardEvents": [{
			"code":"rfpapproved",
			"eventType":"remove",
		},{
			"code":"jopposted",
			"eventType":"remove",
		},{
			"code":"readyforjobposting",
			"eventType":"remove",
		}],
		"prompts": [
			{
				"code": "username",
				"label": "Username",
				"enabled": False,
				"required": False,
				"ldapsearch": False,
			},
			{
				"code": "first_name",
				"label": "First Name",
				"enabled": True,
				"required": True,
				"ldapfield": "givenName",
			},
			{
				"code": "middle_name",
				"label": "Middle Name",
				"enabled": True,
				"required": False,
			},
			{
				"code": "last_name",
				"label": "Last Name",
				"enabled": True,
				"required": True,
				"ldapfield": "sn",
			},
			{
				"code": "suffix",
				"label": "Suffix",
				"enabled": True,
				"required": False,
			},
			{
				"code": "email",
				"label": "Email",
				"enabled": True,
				"required": False,
				"ldapfield": "mail",
			},
			{
				"code": "employee_nbr",
				"label": "Employee Nbr",
				"enabled": False,
				"required": False,
			},
		],
		"activityLog": {
			"enabled": True,
			"activityLogText": "Candidate Identified",
		},
	},
}
