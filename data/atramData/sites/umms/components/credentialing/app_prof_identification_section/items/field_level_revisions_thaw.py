# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

field_level_revisions_thaw = {
	"code": "field_level_revisions_thaw",
	"comment":"",
	"descr": "Dehydrator",
	"header": "",
	"componentType": "Task",
	"affordanceType":"",
	"optional": False,
	"enabled": False,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"",
	"className": "FLRR_Activator",
	"config": {
			"approvalTask": "cred_attestation",
			"freeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": ["cred_attestation"],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "cred_attestation",
		},
		"emails": [{
			"sendToUser":False,
			"sendToCandidate":False,
			"sendToDepartment":True,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"subject":"Revisions Required",
			"bodyTemplateName":"field_level_revisions.html",
		}],
		"activityLog": {
			"enabled": False,
		},
	},
}
