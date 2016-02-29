# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_journal_rank = {
	"code": "promo_journal_rank",
	"comment":"",
	"descr": '''Ranking of Journals''',
	"header": '''Ranking of Journals''',
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
	"successMsg":"Ranking of Journals Complete",
	"className": "FileUpload",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Ranking of Journals",
		},
		"min": "1",
		"max": "1",
	},
}
