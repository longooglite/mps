# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

promotion_container = {
	"code": "promotion_container",
	"descr": "Promotion",
	"header": "Promotion",
	"componentType": "Container",
    "affordanceType":"Tab",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ['recruitment_container'],
	"statusMsg": "Ready for OFA",
	"className": "Container",
	"containers": ["promo_blocking_container","promo_fa_packet_section"]
}
