# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_int_regents_section = {
	"code": "sec_int_regents_section",
	"descr": "Regents",
	"header": "Regents",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["sec_int_assist_dean_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["regents_vote"]
}
