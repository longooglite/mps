# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

enroll_reviewed_by_dept = {
	"code": "enroll_reviewed_by_dept",
	"descr": "Reviewed and Returned by Department",
	"header": "Reviewed and Returned by Department",
	"componentType": "Task",
	"affordanceType":"Item",
	"overviewOnly":True,
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["dept_task"],
	"viewPermissions": ["ofa_task","dept_task","enroll_task"],
	"blockers": ["submitOFA"],
	"statusMsg": "",
	"successMsgApprove":"Enrollment Packet Approved",
	"successMsgDeny":"",
	"successMsgRevisions":"",
	"className": "Approval",
	"config": {
		"approve": True,
		"approveText": "Approve",
		"approveStatusMsg": "Enrollment Packet Approved",
		"approveFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": [],
			"setJobActionRevisionsRequired": False,
			"clearJobActionRevisionsRequired": True,
			"clearSubmitStatus": "",
			"activityLogText": "Approved",
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Enrollment Packet Approved",
			"comments": [
				{
					"commentCode": "enrollmentpacketapprovalCommentEverybody",
					"commentLabel": "Comment",
					"accessPermissions": ["dept_task"],
					"viewPermissions": ["ofa_task","dept_task","enroll_task"],
				},
			],
		},
		"vote": False,
	},
}
