# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_provider_change_form = {
	"code": "enroll_provider_change_form",
	"comment":"",
	"descr": '''<a class="wf-external-link" href="http://www.med.umich.edu/mss/privileges.htm" target="_blank">Download Provider Change Form</a>''',
	"header": '''<a class="wf-external-link" href="http://www.med.umich.edu/mss/privileges.htm" target="_blank">Download Provider Change Form</a>''',
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": True,
	"enabled": True,
	"accessPermissions": ["dept_task","apptCandidate"],
	"viewPermissions": ["dept_task","enroll_task","ofa_task","apptCandidate"],
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
