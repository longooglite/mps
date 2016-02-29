# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

npi = {
	"code": "npi",
	"descr": "National Provider Identifier Information",
	"header": "National Provider Identifier Information",
	"componentType": "Task",
    "affordanceType":"Item",
	"optional": False,
	"enabled": True,
	"accessPermissions": ["apptCandidate"],
	"viewPermissions": ["dept_task","ofa_task","apptCandidate","mss_task"],
	"blockers": ["startappointment"],
	"containers": [],
    "statusMsg": "",
	"successMsg":"NPI saved",
	"className": "NPI",
	"config": {
		"parentCode": "npi",
		"form":"ummsnpi.html",
		"npipdf":"ummsnpiform.pdf",
		"pdfUserNamePageNbrs":[2],
		"formfillPDFMapping":[('2 First_2','Ellen'),
          ('3 Middle_2','J.'),
          ('4 Last_2','Kayfes'),
          ('7 TitlePosition_2',''),
          ('8 EMail Address','ProviderEnrollKMS@med.umich.edu'),
          ('9 Telephone Number Include Area Code','734-936-2047')],
		"institution_name":"University of Michigan Provider Enrollment",
		"prompts": [
			{
				"code": "npi_nbr",
				"label": "NPI #",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "does_not_have_npi",
				"label": "",
				"enabled": True,
				"required": True,
				"data_type": "checkbox",
			},
			{
				"code": "npi_username",
				"label": "Username",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "npi_password",
				"label": "Password",
				"enabled": True,
				"required": True,
				"data_type": "string",
			},
			{
				"code": "agree",
				"label": "",
				"enabled": True,
				"required": True,
				"data_type": "checkbox",
			},

		],

	},

}
