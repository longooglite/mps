# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

acad_eval_section = {
	"code": "acad_eval_section",
	"descr": "Academic Evaluations",
	"header": "Academic Evaluations",
	"componentType": "Container",
	"affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ["promotion_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["req_participate","manage_evals"]
}
