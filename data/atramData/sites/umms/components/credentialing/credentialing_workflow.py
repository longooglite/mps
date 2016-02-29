# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

credentialing_workflow = {
	"code": "credentialing_workflow",
	"descr": "Credentialing",
	"header": "Credentialing",
	"componentType": "Workflow",
	"affordanceType":"",
    "metaTrackCodes":["Faculty","Lecturer","Supplemental"],
    "jobActionType":"CREDENTIAL",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "Started",
	"className": "Container",
	"containers": ["app_prof_ident_tab","edu_train_serv_clinical_ass_tab","review_approval_tab"],
	"config": {
		"proposed_start_date_change_alert": {
			"sendToUser":False,
			"sendToDepartment":True,
			"sendToSitePref":[],
			"sendToAddresses":[],
			"sendToCCAddresses":[],
			"sendToBCCAddresses":[],
			"emailTextComplete":"Clinical Start Date Changed from %s to %s",
			"alwaysSend":True,
		},
		"FLRR_Container":"field_level_revisions_thaw",
		"initItemCodes":["cred_personalinfo","ari","cbc","npi"],
	},
}
