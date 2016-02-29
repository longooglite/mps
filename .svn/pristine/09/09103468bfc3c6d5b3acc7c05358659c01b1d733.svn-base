# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

internaleval = {
	"code": "internaleval",
	"comment":"",
	"descr": "Notify Internal Reviewers",
	"header": "Notify Internal Reviewers",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"accessPermissions": ["dept_task","mss_task"],
	"viewPermissions": ["dept_task","mss_task","ofa_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"",
	"className": "Evaluations",

	"config": {
		"evaluatorTextMC":"Reviewer",
		"evaluationTextMC":"Review",
		"evaluationTextLC":"review",
		"requiresResponses":False,
		"internalEvaluatorImport":True,
		"packet_code":"packetABC",
		"add_num_pages_toc_specifier": False,
		"add_last_page_toc_entry": False,
		"title":"Packet Review",
		"packetEnabled": True,
		"packetText": "Download Packet",
		"reviewersEnabled": False,
		"reviewersText": "",
		"letterEnabled": False,

		"emailTemplateName": "internalReviewerSolicit.html",
		"emailSubjectLine": "Request for Packet Review",
		"emailSendBlockers": [],

		"headerImageOverride":"cred_default_head.png",
		"omitCodes": [],
		"printHeader": "Notify Internal Reviewers",

		"addEvalDashboardEvents": [],
		"removeEvalDashboardEvents":[],
		"activityLog": {
			"enabled": False,
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
					"commentLabel": "Please enter a reason for declining this evaluator",
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
			"activityLogText": "Add Reviewer",
		},
		"editActivityLog": {
			"enabled": True,
			"activityLogText": "Edit Reviewer",
		},
		"declineActivityLog": {
			"enabled": True,
			"activityLogText": "Decline Evaluator",
		},
		"deleteActivityLog": {
			"enabled": True,
			"activityLogText": "Delete Reviewer",
		},
		"sendActivityLog": {
			"enabled": True,
			"activityLogText": "Send Reviewer Email",
		},
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "Evaluator Form Submission",
		},
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "Evaluator Form Submission (draft)",
		},
		"approveActivityLog": {
			"enabled": True,
			"activityLogText": "Evaluator Approved",
		},
		"denyActivityLog": {
			"enabled": True,
			"activityLogText": "Evaluator Denied",
		},

		"deleteCommentCode": "deleteComment",
		"declineCommentCode": "declineComment",
		"reviewCommentCode": "reviewComment",

		"min": "1",
		"max": "10",
		"showMaxAllowed":False,
		"evaluatorSources": [],
		"evaluatorTypes": [],
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
				"enabled": False,
				"required": False,
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
				"enabled": False,
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
				"enabled": False,
				"required": False,
				"data_type": "string",
			},
			{
				"code": "degree",
				"label": "Degree",
				"enabled": False,
				"required": False,
				"data_type": "string",
			},
			{
				"code": "salutation",
				"label": "Salutation",
				"enabled": False,
				"required": False,
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
				"enabled": False,
				"required": False,
				"data_type": "string",
			},
			{
				"code": "titles",
				"label": "Title",
				"enabled": False,
				"required": False,
				"data_type": "list",
			},
			{
				"code": "institution",
				"label": "Institution",
				"enabled": False,
				"required": False,
				"data_type": "string",
			},
			{
				"code": "reason",
				"label": "Evaluator Bio/Reason for Selection",
				"enabled": False,
				"required": False,
				"data_type": "string",
			},
		],
	},
}
