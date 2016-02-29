# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_provost_section = {
	"code": "promo_provost_section",
	"descr": "Provost",
	"header": "Provost",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ["approveOFA","promo_advisory_section","promo_assist_dean_section","promo_exec_com_section","promo_dean_section","promo_evpma_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["promorec","provost_promo_packet","provost_submit_date","promo_provost_vote"]
}
