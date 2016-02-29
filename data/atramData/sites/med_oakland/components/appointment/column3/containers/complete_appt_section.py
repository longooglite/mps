# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

complete_appt_section = {
	"code": "complete_appt_section",
	"descr": "Complete Appointment",
	"header": "Complete Appointment",
	"componentType": "Container",
	"affordanceType":"Section",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ["bot_review_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["create_appt_letter","signed_appt_letter","ou_personnel_form","ou_general_terms","send_ppap_forms","complete_ppap_forms","complete_appointment"]
}
