# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

edu_train_serv_clinical_ass_tab = {
	"code": "edu_train_serv_clinical_ass_tab",
	"descr": "Education, Training, Service, Clinical Assessments",
	"header": "Education, Training, Service, Clinical Assessments",
	"componentType": "Container",
    "affordanceType":"Tab",
	"optional": False,
	"enabled": True,
	"accessPermissions": [],
	"viewPermissions": [],
	"blockers": ["prerequisite_section"],
	"statusMsg": "",
	"className": "Container",
	"containers": ["professional_edu_section","post_grad_section","serv_rank_section","tricare_section","clinical_assessment_section"]
}
