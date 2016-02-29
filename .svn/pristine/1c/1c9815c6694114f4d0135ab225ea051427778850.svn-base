# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#   MPS CV Menues.

MENUES = \
[
	{
		"descr": "CV Home",
		"rootid":"home",
		"enabled":"true",
		"permissions": [],
		"glyph": "glyphicon-home",
		"url": "/cv"
	},
	{
		"descr": "Print",
		"rootid":"print",
		"enabled":"false",
		"permissions": [],
		"glyph": "glyphicon-print",
		"itemList": [
			{
				"descr": "Print All",
				"url": "/cv/print/{cvCommunity}/{cvOwner}",
				"target": "_blank",
				"enabled":"false",
				"permissions": ['cvView']
			},
			{
				"descr": "Print Section",
				"url": "/cv/print/{cvCommunity}/{cvOwner}/{categoryCode}",
				"target": "_blank",
				"enabled":"false",
				"permissions": ['cvView']
			},
		]
	},
	{
		"descr": "Manage External Data",
		"rootid":"manageexternaldata",
		"enabled":"false",
		"permissions": ['cvEdit'],
		"glyph": "glyphicon-cloud-download",
		"itemList": [
			{
				"descr": "PubMed",
				"url": "/cv/pubmed/view/{cvCommunity}/{cvOwner}",
				"enabled":"false",
				"permissions": ['cvEdit']
			},
			{
				"descr": "Export as JSON",
				"url": "/cv/exportjson/{cvCommunity}/{cvOwner}",
				"target": "_blank",
				"enabled":"false",
				"permissions": ['cvExport']
			},
			{
				"descr": "Import CV",
				"url": "/cv/import/{cvCommunity}/{cvOwner}",
				"enabled":"false",
				"permissions": ['cvExport']
			},
		]
	},
	{
		"descr": "Admin",
		"rootid":"admin",
		"enabled":"true",
		"permissions": ['cvAdmin'],
		"glyph": "glyphicon-wrench",
		"itemList": [
			{
				"descr": "Users",
				"url": "/cv/users",
				"enabled":"true",
				"permissions": ['cvAdmin']
			},
		]
	},
]

