# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

dcapt_approval_section = {
	"code": "dcapt_approval_section",
	"descr": "DCAPT Approval",
	"header": "DCAPT Approval",
	"componentType": "Container",
	"affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ["chair_review_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["dcapt_casebook","dcapt_vote","dcapt_recommend","submit_faculty_affairs"]
}
