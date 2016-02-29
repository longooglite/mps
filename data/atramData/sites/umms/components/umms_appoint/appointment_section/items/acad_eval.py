# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

acad_eval = {
	"code": "acad_eval",
	"comment":"this... is academic evaluations",
	"descr": "Academic Evaluations",
	"header": "Academic Evaluations",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"accessPermissions": ["ofa_task","dept_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": [],
	"containers": [],
	"statusMsg": "Academic References Complete",
	"className": "Evaluations",
	"config": {
		"addEvalDashboardEvents": [{
			"code":"eval_review",
			"sortOrder":"j1",
			"eventDescription":"Arm's Length Ready for Review",
			"evaluatorTypes":["AL_EXTERNAL","AL_INTERNAL"],
			"eventType":"create",
			"permission":["ofa_task"]
		},{
			"code":"arisubmit",
			"eventType":"remove",
		}],
		"removeEvalDashboardEvents":[{
			"code":"eval_review",
			"eventType":"remove",
			"permission":["eval_review"]
		}],
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
			"activityLogText": "Add Evaluator",
		},
		"editActivityLog": {
			"enabled": True,
			"activityLogText": "Edit Evaluator",
		},
		"declineActivityLog": {
			"enabled": True,
			"activityLogText": "Decline Evaluator",
		},
		"deleteActivityLog": {
			"enabled": True,
			"activityLogText": "Delete Evaluator",
		},
		"sendActivityLog": {
			"enabled": True,
			"activityLogText": "Send Solicitation Email",
		},
		"uploadActivityLog": {
			"enabled": True,
			"activityLogText": "Evaluator File Upload",
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

		"min": "3",
		"max": "10",
		"showMaxAllowed":False,
		"evaluatorSources": [
			{
				"code": "CANDIDATE",
				"min": "0",
				"max": "50",
			},
			{
				"code": "CHAIR",
				"min": "1",
				"max": "50",
			},
		],
		"evaluatorTypes": [
			{
				"code": "AL_EXTERNAL",
				"min": "0",
				"max": "50",
			},
			{
				"code": "AL_INTERNAL",
				"min": "0",
				"max": "50",
			},
			{
				"code": "NAL_EXTERNAL",
				"min": "0",
				"max": "50",
			},
			{
				"code": "NAL_INTERNAL",
				"min": "0",
				"max": "50",
			},
		],
		"evaluatorTypeCollections": [
			{
				"codes": ["AL_EXTERNAL","AL_INTERNAL"],
				"descr": "Arm's Length",
				"min": "0",
				"max": "50",
			},
		],

		"prompts": [
			{
				"code": "evaluator_source",
				"label": "Suggested by",
				"enabled": True,
				"required": True,
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

		"emailTemplateName": "ummsacadSolicit.html",
		"emailSubjectLine": "Letter of Recommendation Request",
		"emailSendBlockers": ["solicitation_section","promo_solicitation_section"],

		"reviewPermissions": ['ofa_task'],

		"packet_code": "solicitation_packet",
		"add_num_pages_toc_specifier": False,
		"add_last_page_toc_entry": False,
		"title":"SOLICITATION PACKET",

		"packetEnabled": True,
		"packetText": "View/Download Solicitation Packet",
		"reviewersEnabled": True,
		"reviewersText": "View/Download Reviewers List",
		"letterEnabled": True,
		"letterText": "View/Download Letter",
	},
}
