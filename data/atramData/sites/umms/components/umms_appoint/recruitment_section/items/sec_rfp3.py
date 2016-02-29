# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_rfp3 = {
	"code": "sec_rfp3",
	"descr": "Secondary RFP",
	"header": "Secondary RFP",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task","ofa_task","mss_task"],
	"blockers": ["sec_confirm_title3"],
	"statusMsg": "Secondary RFP Started",
	"successMsg": "Secondary RFP saved",
	"successMsgDraft": "Secondary RFP draft saved",
	"className": "UberForm",
	"config": {
		"disclosureGroup": { "code": "sec3", "descr": "3rd Secondary Appointment" },
		"questionGroupCode": "secondaryRFP",
		"omitCodes": [],

		"submitEnabled": True,
		"submitText": "Save",
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "Secondary RFP saved",
		},

		"draftEnabled": True,
		"draftText": "Save as Draft",
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "Secondary RFP saved as draft",
		},
	},
}