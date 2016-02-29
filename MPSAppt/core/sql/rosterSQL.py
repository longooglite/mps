# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

def getRawRosterData(_connection):
	sql = '''SELECT
		POS.id AS position_id,
		POS.pcn AS pcn,
		POS.is_primary AS is_primary,
		POS.department_id AS department_id,
		POS.title_id AS position_title_id,
		APPT.id AS appointment_id,
		APPT.title_id AS appointment_title_id,
		APPT.start_date AS start_date,
		APPT.end_date AS end_date,
		APPT.appointment_status_id AS appointment_status_id,
		JA.id AS job_action_id,
		JA.workflow_id AS workflow_id,
		JA.updated AS job_action_updated,
		JA.current_status AS job_action_status,
		JA.proposed_start_date AS proposed_start_date,
		JA.frozen AS frozen,
		JA.revisions_required AS revisions_required,
		PERSON.id AS person_id,
		PERSON.username AS username,
		PERSON.first_name AS first_name,
		PERSON.middle_name AS middle_name,
		PERSON.last_name AS last_name,
		PERSON.suffix AS suffix,
		PERSON.email AS email
	FROM wf_position AS POS
		JOIN wf_department AS DEPT
		ON DEPT.id = POS.department_id
		LEFT OUTER JOIN wf_appointment AS APPT
			LEFT OUTER JOIN wf_person AS PERSON
			ON APPT.person_id = PERSON.id
			LEFT OUTER JOIN wf_job_action AS JA
			ON JA.appointment_id = APPT.id
		ON APPT.position_id = POS.id
			AND APPT.appointment_status_id IN (SELECT id FROM wf_appointment_status WHERE code IN ('FILLED','INPROGRESS'))
	ORDER BY POS.is_primary DESC, POS.pcn, APPT.appointment_status_id DESC'''
	return _connection.executeSQLQuery(sql)
