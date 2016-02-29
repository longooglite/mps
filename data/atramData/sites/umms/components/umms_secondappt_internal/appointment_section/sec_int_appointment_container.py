# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

sec_int_appointment_container = {
	"code": "sec_int_appointment_container",
	"descr": "Appointment",
	"header": "Appointment",
	"componentType": "Container",
    "affordanceType":"Tab",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ["sec_int_recruitment_container"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["sec_int_remaining_uploads_section","sec_int_fa_packet_section"]
}
