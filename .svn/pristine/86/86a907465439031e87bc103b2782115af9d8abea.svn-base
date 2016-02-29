# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_ext_start_appointment = {
	"code": "sec_ext_start_appointment",
	"descr": "Enter UM Identity",
	"header": "Enter UM Identity",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task","ofa_task"],
	"overviewOnly":False,
	"blockers": ["signed_offer"],
	"statusMsg": "Pre-Hire Started",
	"successMsg": "Identity verified - email sent",
	"className": "IdentifyCandidate",
	"config": {
		"emails": [{
			"sendToUser":False,
			"sendToDepartment":False,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"subject":"Welcome to the University of Michigan Medical School Pre-Hire Process",
			"bodyTemplateName":"prehire_start.html",
		}],
		"prompts": [
			{
				"code": "community",
				"label": "Community",
				"enabled": True,
				"required": True,
			},
			{
				"code": "username",
				"label": "Username",
				"enabled": True,
				"required": True,
				"ldapsearch": True,
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
				"required": True,
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
			"activityLogText": "Start Secondary Appointment",
		},
	},
}
