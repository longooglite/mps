# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

solicit_references = {
	"code": "solicit_references",
	"comment":"",
	"descr": '''Solicit References''',
	"header": '''Solicit References''',
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
	"successMsg":"Solicit References Complete",
	"className": "Evaluations",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Only used as a comment template, do not enable",
			"comments": [
				{
					"commentCode": "deleteComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task","dept_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
				{
					"commentCode": "declineComment",
					"commentLabel": "Please enter a reason for declining this reviewer",
					"accessPermissions": ["ofa_task","dept_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
				{
					"commentCode": "reviewComment",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task","dept_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
		"addActivityLog": {
			"enabled": True,
			"activityLogText": "Add Reference",
		},
		"editActivityLog": {
			"enabled": True,
			"activityLogText": "Edit Reference",
		},
		"declineActivityLog": {
			"enabled": True,
			"activityLogText": "Decline Reference",
		},
		"deleteActivityLog": {
			"enabled": True,
			"activityLogText": "Delete Reference",
		},
		"sendActivityLog": {
			"enabled": True,
			"activityLogText": "Send Solicitation Email",
		},
		"uploadActivityLog": {
			"enabled": True,
			"activityLogText": "Reference File Upload",
		},
		"approveActivityLog": {
			"enabled": True,
			"activityLogText": "Reference Approved",
		},
		"denyActivityLog": {
			"enabled": True,
			"activityLogText": "Reference Denied",
		},

		"deleteCommentCode": "deleteComment",
		"declineCommentCode": "declineComment",
		"reviewCommentCode": "reviewComment",

		"min": "0",
		"max": "999",
		"showMaxAllowed":False,
		"evaluatorSources": [],
		"evaluatorTypes": [
			{
				"code": "EXTERNAL",
				"min": "0",
				"max": "999",
			},
			{
				"code": "INTERNAL",
				"min": "0",
				"max": "999",
			},
		],
		"evaluatorTypeCollections": [],

		"prompts": [
			{
				"code": "evaluator_source",
				"label": "Suggested by",
				"enabled": False,
				"required": False,
				"data_type": "string",
			},
			{
				"code": "evaluator_type",
				"label": "Evaluator Type",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "first_name",
				"label": "First Name",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "middle_name",
				"label": "Middle Name",
				"enabled": True,
				"required": False,
				"data_type": "string",
			},
			{
				"code": "last_name",
				"label": "Last Name",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "suffix",
				"label": "Suffix",
				"enabled": True,
				"required": False,
				"data_type": "string",
			},
			{
				"code": "degree",
				"label": "Degree",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "salutation",
				"label": "Salutation",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "email",
				"label": "Email",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "phone",
				"label": "Phone",
				"enabled": True,
				"required": False,
				"data_type": "string",
			},
			{
				"code": "titles",
				"label": "Academic Title",
				"enabled": True,
				"required": True,
				"data_type": "list",
			},
			{
				"code": "institution",
				"label": "Institution",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "reason",
				"label": "Evaluator Bio/Reason for Selection",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
		],

		"emailTemplateName": "med-oakland_solicit_references.html",
		"emailSubjectLine": "Reference Request",
		"emailSendBlockers": [],

		"reviewPermissions": ['ofa_task'],

		"packet_code": "some_casebook",
		"add_num_pages_toc_specifier": False,
		"add_last_page_toc_entry": False,
		"title":"REFERENCE PACKET",

		"packetEnabled": True,
		"packetText": "View/Download Reference Packet",
		"reviewersEnabled": True,
		"reviewersText": "View/Download Reference List",
		"letterEnabled": True,
		"letterText": "View/Download Letter",
	},
}
