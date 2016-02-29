# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

cred_application_submit = {
	"code": "cred_application_submit",
	"descr": "Submit Credentialing Application",
	"header": "Submit Credentialing Application",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ['apptCandidate'],
	"viewPermissions": ['dept_task','ofa_task','apptCandidate','mss_task'],
	"overviewOnly":False,
	"blockers": ["app_blocking_container"],
	"statusMsg": "Application Submitted",
	"successMsg": "Application Submitted",
	"className": "Submit",
	"config": {
		"instructional":"Please make sure everything you have entered is accurate then press submit to finalize your entries.",
		"submitText": "Submit",
		"submitFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": True,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Credentialing Application Submitted",
			"comments": [
				{
					"commentCode": "submitApplication",
					"commentLabel": "Comment",
					"accessPermissions": ["apptCandidate"],
					"viewPermissions": ["apptCandidate","ofa_task","dept_task","mss_task"],
				},
			],
		},
	},
}
