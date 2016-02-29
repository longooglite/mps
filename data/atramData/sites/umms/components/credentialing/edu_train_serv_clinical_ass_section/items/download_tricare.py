# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

download_tricare = {
	"code": "download_tricare",
	"comment":"",
	"descr": '''<a class="wf-external-link" href="http://www.med.umich.edu/mss/pdf/TriCareChampus.pdf" target="_blank">Download TriCare Form</a>''',
	"header": '''<a class="wf-external-link" href="http://www.med.umich.edu/mss/pdf/TriCareChampus.pdf" target="_blank">Download TriCare Form</a>''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"accessPermissions": ["dept_task","apptCandidate"],
	"viewPermissions": ["dept_task","mss_task","ofa_task","apptCandidate"],
	"blockers": [],
	"containers": [],
	"statusMsg": "",
	"successMsg":"Download TriCare Form was saved",
	"className": "Placeholder",
	"config": {
		"activityLog": {
			"enabled": True,
			"activityLogText": "Download TriCare Form Placeholder",
		},
	},
}
