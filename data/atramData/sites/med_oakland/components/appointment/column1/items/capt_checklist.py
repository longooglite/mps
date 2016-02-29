# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

capt_checklist = {
	"code": "capt_checklist",
	"comment":"",
	"descr": '''CAPT Checklist''',
	"header": '''CAPT Checklist''',
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
	"successMsg":"CAPT Checklist Complete",
	"className": "UberForm",
	"config": {
		"questionGroupCode": "CAPTChecklistMain",
		"omitCodes": [],

		"submitEnabled": True,
		"submitText": "Save",
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "CAPT Checklist saved",
		},

		"draftEnabled": True,
		"draftText": "Save as Draft",
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "CAPT Checklist saved as draft",
		},

		"savedSetsEnabled": False,
		"savedSetsCreateSuccessMsg": "Template created",
		"savedSetsCreateActivityLog": {
			"enabled": False,
			"activityLogText": "CAPT Checklist template created",
		},
		"savedSetsApplySuccessMsg": "Template applied",
		"savedSetsApplyActivityLog": {
			"enabled": False,
			"activityLogText": "CAPT Checklist template applied",
		},
		"savedSetsDeleteSuccessMsg": "Template deleted",
		"savedSetsDeleteActivityLog": {
			"enabled": False,
			"activityLogText": "CAPT Checklist template deleted",
		},
	},
}
