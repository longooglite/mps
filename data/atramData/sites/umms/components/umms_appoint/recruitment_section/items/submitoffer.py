# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

submitoffer = {
	"code": "submitoffer",
	"descr": "Submit Offer",
	"header": "Submit Offer",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"overviewOnly":False,
	"accessPermissions": ['dept_task'],
	"viewPermissions": ['dept_task','ofa_task',"mss_task"],
	"blockers": ["initialofferletter","identifycandidate","confirmtitle","aar","mou","provojustification"],
	"statusMsg": "Offer Pending Approval",
	"successMsg": "Offer submitted",
	"className": "Submit",
	"config": {
		"dashboardEvents": [{
			"code":"offersubmit",
			"sortOrder":"c1",
			"eventDescription":"Offer Awaiting Approval",
			"eventType":"create",
			"permission":["ofa_task"]
		},{
			"code":"offerrevisions",
			"eventType":"remove",
		},{
			"code":"offerstarted",
			"eventType":"remove",
		},{
			"code":"offerextended",
			"eventType":"remove",
		},{
			"code":"offeraccepted",
			"eventType":"remove",
		},],
		"submitText": "Submit",
		"submitFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": True,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Offer Submitted for Approval",
			"comments": [
				{
					"commentCode": "submitOffer",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
			],
		},
	},
}
