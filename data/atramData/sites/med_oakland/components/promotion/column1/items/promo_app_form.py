# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_app_form = {
	"code": "promo_app_form",
	"comment":"",
	"descr": '''Application Form''',
	"header": '''Application Form''',
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
	"successMsg":"Application Form Complete",
	"className": "UberForm",
	"config": {
		"questionGroupCode": "PromoApplMain",
		"omitCodes": [],

		"submitEnabled": True,
		"submitText": "Save",
		"submitActivityLog": {
			"enabled": True,
			"activityLogText": "Application Form saved",
		},

		"draftEnabled": True,
		"draftText": "Save as Draft",
		"draftActivityLog": {
			"enabled": True,
			"activityLogText": "Application Form saved as draft",
		},

		"savedSetsEnabled": False,
		"savedSetsCreateSuccessMsg": "Template created",
		"savedSetsCreateActivityLog": {
			"enabled": False,
			"activityLogText": "Application Form template created",
		},
		"savedSetsApplySuccessMsg": "Template applied",
		"savedSetsApplyActivityLog": {
			"enabled": False,
			"activityLogText": "Application Form template applied",
		},
		"savedSetsDeleteSuccessMsg": "Template deleted",
		"savedSetsDeleteActivityLog": {
			"enabled": False,
			"activityLogText": "Application Form template deleted",
		},
	},
}
