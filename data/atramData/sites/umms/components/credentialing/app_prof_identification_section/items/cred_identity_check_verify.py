# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_identity_check_verify = {
	"code": "cred_identity_check_verify",
	"comment":"",
	"descr": "Identity Check Verification",
	"header": "Identity Check Verification",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task","ofa_task","mss_task"],
	"blockers": ["cred_upload_image_id","prerequisite_section","cred_release_statement"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Identity check was saved",
	"className": "Attest",
	"config":
	{
		"dashboardEvents": [{
			"code":"credidentity",
			"sortOrder":"a1",
			"eventDescription":"Identity Check Verification Complete",
			"eventType":"create",
			"permission":["mss_task"]
		},],
		"freeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": ["cred_upload_image_id"],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "",
			"activityLogText": "",
		},
		"displayImage":True,
		"displayImageTaskCode":"cred_upload_image_id",
		"displayImageScalePixelWidth":400,
		"prompts": [
			{
				"code": "attest",
				"label": "",
				"enabled": True,
				"required": True,
				"data_type": "checkbox",
			},
		],
		"submitText":"CLICKING SUBMIT MEANS THAT I, {attestor_name}, {attestor_department}, VERIFY THAT THE ABOVE STATEMENT IS CORRECT",
		"form":"umms_identity_check.html",
		"activityLog": {
			"enabled": True,
			"activityLogText": "Identity Check Edited",
		},

	},
}