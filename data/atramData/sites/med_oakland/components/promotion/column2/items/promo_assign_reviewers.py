# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_assign_reviewers = {
	"code": "promo_assign_reviewers",
	"comment":"",
	"descr": '''Assign Primary & Secondary Reviewers''',
	"header": '''Assign Primary & Secondary Reviewers''',
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
	"successMsg":"Assign Primary & Secondary Reviewers Complete",
	"className": "Evaluations",
	"config": {
		"evaluatorTextMC":"Reviewer",
		"evaluationTextMC":"Review",
		"evaluationTextLC":"review",
		"requiresResponses":False,
		"internalEvaluatorImport":True,

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
			"activityLogText": "Add Primary & Secondary Reviewers",
		},
		"editActivityLog": {
			"enabled": True,
			"activityLogText": "Edit Primary & Secondary Reviewers",
		},
		"declineActivityLog": {
			"enabled": True,
			"activityLogText": "Decline Primary & Secondary Reviewers",
		},
		"deleteActivityLog": {
			"enabled": True,
			"activityLogText": "Delete Primary & Secondary Reviewers",
		},
		"sendActivityLog": {
			"enabled": True,
			"activityLogText": "Send Solicitation Email",
		},
		"uploadActivityLog": {
			"enabled": True,
			"activityLogText": "Primary & Secondary Reviewers File Upload",
		},
		"approveActivityLog": {
			"enabled": True,
			"activityLogText": "Primary & Secondary Reviewers Approved",
		},
		"denyActivityLog": {
			"enabled": True,
			"activityLogText": "Primary & Secondary Reviewers Denied",
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
				"code": "PRIMARY",
				"min": "0",
				"max": "999",
			},
			{
				"code": "SECONDARY",
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

		"emailTemplateName": "med-oakland_promo_assign_reviewers.html",
		"emailSubjectLine": "Review Request",
		"emailSendBlockers": [],

		"reviewPermissions": ['ofa_task'],

		"packet_code": "capt_casebook",
		"add_num_pages_toc_specifier": False,
		"add_last_page_toc_entry": False,
		"title":"REVIEWER PACKET",

		"packetEnabled": True,
		"packetText": "View/Download Reviewer Packet",
		"reviewersEnabled": True,
		"reviewersText": "View/Download Reviewers List",
		"letterEnabled": True,
		"letterText": "View/Download Letter",
	},
}
