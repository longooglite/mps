# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_ari = {
	"code": "promo_ari",
	"comment":"",
	"descr": "Authorization, Release and Immunity (ARI)",
	"header": "Authorization, Release and Immunity (ARI)",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate"],
	"blockers": ["startappointment"],
	"containers": [],
	"statusMsg": "",
	"successMsg":"ARI was saved",
	"className": "Attest",
	"config": {
		"dashboardEvents": [{
			"code":"arisubmit",
			"sortOrder":"h1",
			"eventDescription":"ARI Submitted",
			"eventType":"create",
			"permission":["dept_task"]
		}],
		"prompts": [
			{
				"code": "attest",
				"label": "",
				"enabled": True,
				"required": True,
				"data_type": "checkbox",
			},
		],
		"submitText":"CLICKING SUBMIT MEANS THAT I, %s, UNDERSTAND AND AGREE TO ALL OF THE ABOVE TERMS",
		"form":"ummsari.html",
		"activityLog": {
			"enabled": True,
			"activityLogText": "ARI Edited",
		},
		"initItems":[{"findValidAttestation":[{"codes":["ari","promo_ari","cred_ari"],"lookbackDays":180,
		    "emails": [{
			"sendToCandidate":True,
			"sendToUser":False,
			"sendToDepartment":False,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"subject":"Please complete ARI for Promotion",
			"bodyTemplateName":"promotion_start.html",
		}]}]}],
	},
}