# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

appointment_container = {
	"code": "appointment_container",
	"descr": "Appointment",
	"header": "Appointment",
	"componentType": "Container",
    "affordanceType":"Tab",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ['candidatesubmit'],
	"statusMsg": "Ready for OFA",
	"className": "Container",
	"containers": ["appt_blocking_container","fa_packet_section"]
}
