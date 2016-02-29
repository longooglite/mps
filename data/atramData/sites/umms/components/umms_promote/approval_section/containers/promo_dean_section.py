# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_dean_section = {
	"code": "promo_dean_section",
	"descr": "Dean",
	"header": "Dean",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["ofa_task"],
	"viewPermissions": ["ofa_task"],
	"blockers": ["approveOFA","promo_advisory_section","promo_assist_dean_section","promo_exec_com_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["dean_cover"]
}
