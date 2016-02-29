# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

taskE = {
	"code": "taskE",
	"descr": "Identify Candidate",
	"header": "Identify Candidate",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": [],
	"viewPermissions": ["viewE"],
	"blockers": ["approvalD"],
	"statusMsg": "Candidate identified",
	"className": "IdentifyCandidate",
	"config": {
		"prompts": [
			{
				"code": "username",
				"label": "Username",
				"enabled": True,
				"required": True,
				"ldapsearch": False
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
			"activityLogText": "IdentifyCandidate",
		},
	},
}
