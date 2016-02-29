# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

termination_workflow = {
	"code": "termination_workflow",
	"descr": "Termination",
	"header": "Termination",
	"componentType": "Workflow",
	"affordanceType":"",
	"metaTrackCodes":["Standard","Tenured","TenureTrack"],
	"jobActionType":"TERMINATE",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": [],
	"statusMsg": "Started",
	"className": "Container",
	"containers": ["termination_tab"],
	"terminationItemCode":"termination_item",
}
