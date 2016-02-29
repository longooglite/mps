# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

#   MPS Administration Menues.

MENUES = \
[
	{
		"descr": "Sessions",
		"rootid":"sessions",
		"enabled":"true",
		"url": "/admin/sessions",
		"glyph": "glyphicon-eye-open",
		"permissions": ['sessionView']
	},
	{
		"descr": "Entities",
		"rootid":"entities",
		"enabled":"true",
		"permissions": [],
		"glyph": "glyphicon-globe",
		"itemListHasGlyphs": True,
		"itemList": [
			{
				"descr": "Sites",
				"enabled":"true",
				"url": "/admin/sites",
				"glyph": "glyphicon-globe",
				"permissions": ['siteView']
			},
			{
				"descr": "Communities",
				"enabled":"true",
				"url": "/admin/communities",
				"glyph": "glyphicon-cutlery",
				"permissions": ['communityView']
			},
			{
				"descr": "Preferences",
				"enabled":"true",
				"url": "/admin/prefs",
				"glyph": "glyphicon-cog",
				"permissions": ['prefView']
			},
			{
				"descr": "Roles",
				"enabled":"true",
				"url": "/admin/roles",
				"glyph": "glyphicon-lock",
				"permissions": ['roleView']
			},
			{
				"descr": "Users",
				"enabled":"true",
				"url": "/admin/users",
				"glyph": "glyphicon-user",
				"permissions": ['userView']
			},
		]
	},
	{
		"descr": "Database",
		"rootid":"db",
		"enabled":"true",
		"permissions": [],
		"glyph": "glyphicon-hdd",
		"itemListHasGlyphs": True,
		"itemList": [
			{
				"descr": "Dump",
				"enabled":"true",
				"url": "/admin/db/dump",
				"glyph": "glyphicon-save",
				"permissions": ['dbDump']
			},
			{
				"descr": "Restore",
				"enabled":"true",
				"url": "/admin/db/restore",
				"glyph": "glyphicon-open",
				"permissions": ['dbRestore']
			},
		]
	},
	{
		"descr": "Caches",
		"rootid":"misc",
		"enabled":"true",
		"permissions": [],
		"glyph": "glyphicon-list-alt",
		"itemListHasGlyphs": True,
		"itemList": [
			{
				"descr": "Clear Site Cache",
				"id": "clearSiteCacheMenuItem",
				"enabled":"true",
				"permissions": ['siteView'],
				"glyph": "glyphicon-globe",
			},
			{
				"descr": "Clear User Cache",
				"id": "clearUserCacheMenuItem",
				"enabled":"true",
				"permissions": ['userView'],
				"glyph": "glyphicon-user",
			},
			{
				"descr": "Clear Session Cache",
				"id": "clearSessionCacheMenuItem",
				"enabled":"true",
				"permissions": ['sessionView'],
				"glyph": "glyphicon-eye-open",
			}
		]
	},
]
