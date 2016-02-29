# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promo_regents_section = {
	"code": "promo_regents_section",
	"descr": "Regents",
	"header": "Regents",
	"componentType": "Container",
    "affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ["approveOFA","promo_advisory_section","promo_assist_dean_section","promo_exec_com_section","promo_dean_section","promo_evpma_section","promo_provost_section","promo_vp_research_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["promo_regents_vote"]
}
