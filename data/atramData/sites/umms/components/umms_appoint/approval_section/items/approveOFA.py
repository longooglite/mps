# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

approveOFA = {
	"code": "approveOFA",
	"descr": "OFA Approval",
	"header": "OFA Approval",
	"componentType": "Task",
	"affordanceType":"Item",
	"overviewOnly":True,
	"optional": False,
	"enabled": True,
	"logEnabled": True,
	"freezable": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task","dept_task","mss_task"],
	"blockers": ["submitOFA"],
	"statusMsg": "",
	"successMsgApprove":"OFA Appointment Approved",
	"successMsgDeny":"OFA Appointment Denied",
	"successMsgRevisions":"OFA Appointment Revisions Required",
	"className": "Approval",
	"config": {
		"data-confirm-msg":"Please confirm. You cannot undo this action.",
		"approve": True,
		"approveDashboardEvents": [{
			"code":["ofapacketsubmit","ofapacketrevisions","deptpacketrevisions"],
			"eventType":"remove",
		},{
			"code":"ofapacketapproved",
			"sortOrder":"p1",
			"component_precondition":"assist_dean_approval",
			"eventDescription":"OFA Review Complete",
			"eventType":"create",
			"permission":["assist_dean_task"]
		},{
			"code":"ofapacketapproved",
			"sortOrder":"p1",
			"eventDescription":"OFA Review Complete",
			"eventType":"create",
			"permission":["ofa_task"]
		}],
		"denyDashboardEvents": [{
			"code":"ofapacketsubmit",
			"eventType":"remove",
		},{
			"code":"ofapacketdenied",
			"sortOrder":"p3",
			"eventDescription":"Packet Not Approved",
			"eventType":"create",
			"permission":["dept_task"]
		}],
		"revisionsDashboardEvents": [{
			"code":["ofapacketsubmit","ofapacketrevisions","deptpacketrevisions"],
			"eventType":"remove",
		},{
			"code":"deptpacketrevisions",
			"sortOrder":"p2",
			"eventDescription":"Packet Revisions Required",
			"eventType":"create",
			"permission":["dept_task"]
		}],
		"approveText": "Approve",
		"approveStatusMsg": "OFA Review Complete",
		"approveFreeze": {
			"freezeJobAction": False,
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
			"activityLogText": "Approved",
		},
		"deny": True,

		"denyText": "Deny",
		"denyStatusMsg": "Denied",
		"denyFreeze": {
			"confirmDeny":True,
			"freezeJobAction": True,
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
			"activityLogText": "Denied",
		},
		"revisionsRequired": True,
		"revisionsRequiredText": "Revisions Required",
		"revisionsRequiredStatusMsg": "Revisions Required",
		"revisionsRequiredFreeze": {
			"freezeJobAction": False,
			"freezeSelf": False,
			"freezeAllPredecessors": False,
			"freezeTasks": [],
			"unfreezeJobAction": False,
			"unfreezeSelf": False,
			"unfreezeAllPredecessors": False,
			"unfreezeTasks": ["submitOFA"],
			"unfreezeOptions": ["signed_offer","aar","mou","provojustification","curriculum_vitae","bib_notes","recent_sig_pubs","acad_eval",
			                    "teaching_eval","formb","transmittal","edu_portfolio","rsrch_portfolio","talking_pts","rs1","rs2",
			                    "cs_summarized_evals","external_solicit","teaching_activity_form","retirement_memoir"],
			"setJobActionRevisionsRequired": True,
			"clearJobActionRevisionsRequired": False,
			"clearSubmitStatus": "submitOFA",
			"activityLogText": "Revisions Required",
		},
		"activityLog": {
			"enabled": True,
			"activityLogText": "Packet Approved",
			"comments": [
				{
					"commentCode": "packetapprovalCommentEverybody",
					"commentLabel": "Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task","dept_task"],
				},
				{
					"commentCode": "packetapprovalCommentOnlyOFA",
					"commentLabel": "OFA-only Comment",
					"accessPermissions": ["ofa_task"],
					"viewPermissions": ["ofa_task"],
				},
			],
		},
		"activityLogTaskCodes": ["approveOFA","submitOFA","assist_dean_approval","advisory_vote","exec_com_vote","evpma_vote","provost_vote","vp_research_vote","regents_vote"],
		"vote": False,
	},
}
