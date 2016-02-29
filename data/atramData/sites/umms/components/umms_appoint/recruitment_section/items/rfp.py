# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

rfp = {
	"code": "rfp",
	"descr": "RFP",
	"header": "RFP",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["dept_task","ofa_task","mss_task"],
	"blockers": [],
	"statusMsg": "RFP Started",
	"successMsg": "RFP saved",
	"successMsgDraft": "RFP draft saved",
	"className": "UberForm",
	"config": {
		"questionGroupCode": "primaryRFP",
		"omitCodes": [],

		"submitEnabled": True,
		"submitText": "Save",
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "RFP saved",
		},

		"draftEnabled": True,
		"draftText": "Save as Draft",
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "RFP saved as draft",
		},

		"savedSetsEnabled": True,
		"savedSetsCreateSuccessMsg": "Template created",
		"savedSetsCreateActivityLog": {
			"enabled": False,
			"activityLogText": "RFP template created",
		},
		"savedSetsApplySuccessMsg": "Template applied",
		"savedSetsApplyActivityLog": {
			"enabled": False,
			"activityLogText": "RFP template applied",
		},
		"savedSetsDeleteSuccessMsg": "Template deleted",
		"savedSetsDeleteActivityLog": {
			"enabled": False,
			"activityLogText": "RFP template deleted",
		},
	},
}
