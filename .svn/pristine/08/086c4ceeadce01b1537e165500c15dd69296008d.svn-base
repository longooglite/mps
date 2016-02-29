# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

acceptoffer = {
	"code": "acceptoffer",
	"descr": "Candidate Response",
	"header": "Candidate Response",
	"componentType": "Task",
	"affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ['dept_task'],
	"viewPermissions": ['ofa_task','dept_task',"mss_task"],
	"blockers": ["extendoffer"],
	"statusMsg": "Offer Accepted",
	"successMsgApprove":"Offer accepted",
	"successMsgDeny":"Offer rejected",
	"className": "Approval",
	"config": {
		"prompts": [
		{
			"code": "approval_date",
			"label": "Date of Response",
			"enabled": True,
			"required": True,
			"data_type": "date",
			"date_format":"M/D/Y"
		}],
		"approve": True,
		"approveDashboardEvents": [{
			"code":"offerextended",
			"eventType":"remove",
		},{
			"code":"offeraccepted",
			"sortOrder":"f1",
			"eventDescription":"Offer Accepted",
			"eventType":"create",
			"permission":["dept_task"]
		}],

		"approveText": "Accept",
		"approveStatusMsg": "Offer Accepted",
		"approveFreeze": {
			"freezeJobAction": False,
			"freezeSelf": True,
			"freezeAllPredecessors": True,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "",
			"activityLogText": "Offer Accepted",
		},
		"deny": True,
		"denyDashboardEvents": [{
			"code":"offerextended",
			"eventType":"remove",
		},{
			"code":"offerrejected",
			"sortOrder":"f2",
			"eventDescription":"Offer Rejected",
			"eventType":"create",
			"permission":["dept_task"]
		}],

		"denyText": "Decline",
		"denyStatusMsg": "Offer Declined",
		"denyFreeze": {
			"freezeJobAction": True,
			"freezeSelf": False,
			"freezeAllPredecessors": True,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
			"activityLogText": "Offer Declined",
		},
		"revisionsRequired": False,
		"activityLog": {
			"enabled": True,
			"activityLogText": "Candidate Response",
			"comments": [],
		},
		"activityLogTaskCodes": ["acceptoffer","extendoffer"],
		"vote": False,
		"date": True,
		"dateText": "Date of Response",
		"dateRequired": True,
	},
}
