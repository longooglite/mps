SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

-- ATRAM --

CREATE TABLE wf_metatrack
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	supplemental boolean NOT NULL,
	active boolean NOT NULL,
	tags VARCHAR NOT NULL
	);
ALTER TABLE wf_metatrack ADD CONSTRAINT wf_metatrack_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_metatrack_code_index ON wf_metatrack (code);


CREATE TABLE wf_track
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	active boolean NOT NULL,
	metatrack_id INT,
	tags VARCHAR NOT NULL
	);
ALTER TABLE wf_track ADD CONSTRAINT wf_track_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_track_code_index ON wf_track (code);
CREATE INDEX wf_track_active_index ON wf_track (active);
ALTER TABLE ONLY wf_track ADD CONSTRAINT wf_track_metatrack_fk
	FOREIGN KEY (metatrack_id) REFERENCES wf_metatrack(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_title
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	active boolean NOT NULL,
	isactionable boolean NOT NULL,
	job_code VARCHAR NOT NULL,
	track_id INT,
	position_criteria VARCHAR NOT NULL DEFAULT '',
	rank_order INT NOT NULL DEFAULT 0,
	tags VARCHAR NOT NULL
	);
ALTER TABLE wf_title ADD CONSTRAINT wf_title_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_title ADD CONSTRAINT wf_title_track_fk
	FOREIGN KEY (track_id) REFERENCES wf_track(id) DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX wf_title_code_index ON wf_title (code);


CREATE TABLE wf_termination_type
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL
	);
ALTER TABLE wf_termination_type ADD CONSTRAINT wf_termination_type_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_termination_type_code_index ON wf_termination_type (code);


CREATE TABLE wf_pcn
	(id SERIAL,
	code VARCHAR NOT NULL,
	seq INT NOT NULL
	);
ALTER TABLE wf_pcn ADD CONSTRAINT wf_pcn_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_pcn_code_index ON wf_pcn (code);


CREATE TABLE wf_department
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	active boolean NOT NULL,
	parent_id INT,
	pcn_id INT NOT NULL,
	cc_acct_cd VARCHAR NOT NULL,
	email_address VARCHAR NOT NULL,
	header_image VARCHAR NOT NULL,
	address_lines VARCHAR NOT NULL,
	city VARCHAR NOT NULL,
	state VARCHAR NOT NULL,
	postal VARCHAR NOT NULL,
	address_suffix VARCHAR  NOT NULL
	);
ALTER TABLE wf_department ADD CONSTRAINT wf_department_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_department_code_index ON wf_department (code);
CREATE INDEX wf_department_parent_id_index ON wf_department (parent_id);
ALTER TABLE ONLY wf_department ADD CONSTRAINT wf_department_parent_fk
	FOREIGN KEY (parent_id) REFERENCES wf_department(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_department ADD CONSTRAINT wf_department_pcn_fk
	FOREIGN KEY (pcn_id) REFERENCES wf_pcn(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_department_chair
	(id SERIAL,
	department_id INT NOT NULL,
	chair_with_degree VARCHAR NOT NULL,
	chair_signature VARCHAR NOT NULL,
	chair_titles VARCHAR NOT NULL,
	seq INT NOT NULL DEFAULT 0
	);
ALTER TABLE wf_department_chair ADD CONSTRAINT wf_department_chair_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_department_chair ADD CONSTRAINT wf_department_chair_department_fk
	FOREIGN KEY (department_id) REFERENCES wf_department(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_department_chair_department_id_index ON wf_department_chair (department_id);
CREATE INDEX wf_department_chair_seq_index ON wf_department_chair (seq);


CREATE TABLE wf_person
	(id SERIAL,
	community VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	suffix VARCHAR NOT NULL,
	middle_name VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
	employee_nbr VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_person ADD CONSTRAINT wf_person_id PRIMARY KEY (id);
CREATE INDEX wf_person_community_username_index ON wf_person (community, username);


CREATE TABLE wf_username_department
	(id SERIAL,
	community VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	department_id INT NOT NULL
	);
	ALTER TABLE wf_username_department ADD CONSTRAINT wf_username_department_id PRIMARY KEY (id);
	ALTER TABLE ONLY wf_username_department ADD CONSTRAINT wf_username_department_department_fk
		FOREIGN KEY (department_id) REFERENCES wf_department(id) DEFERRABLE INITIALLY DEFERRED;
	CREATE UNIQUE INDEX wf_username_department_community_username_department_index ON wf_username_department (community,username,department_id);


CREATE TABLE wf_position
	(id SERIAL,
	department_id INT NOT NULL,
	title_id INT NOT NULL,
	pcn VARCHAR NOT NULL,
	is_primary boolean NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_position ADD CONSTRAINT wf_position_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_position ADD CONSTRAINT wf_position_department_fk
	FOREIGN KEY (department_id) REFERENCES wf_department(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_position_department_id_index ON wf_position (department_id);
ALTER TABLE ONLY wf_position ADD CONSTRAINT wf_position_title_fk
	FOREIGN KEY (title_id) REFERENCES wf_title(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_position_title_id_index ON wf_position (title_id);
CREATE UNIQUE INDEX wf_position_pcn_index ON wf_position (pcn);


CREATE TABLE wf_appointment_status
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL
	);
ALTER TABLE wf_appointment_status ADD CONSTRAINT wf_appointment_status_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_appointment_status_code_index ON wf_appointment_status (code);


CREATE TABLE wf_appointment
	(id SERIAL,
	person_id INT,
	title_id INT,
	position_id INT,
	start_date VARCHAR NOT NULL,
	end_date VARCHAR NOT NULL,
	appointment_status_id INT NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_appointment ADD CONSTRAINT wf_appointment_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_appointment ADD CONSTRAINT wf_appointment_person_fk
	FOREIGN KEY (person_id) REFERENCES wf_person(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_appointment_person_id_index ON wf_appointment (person_id);

ALTER TABLE ONLY wf_appointment ADD CONSTRAINT wf_appointment_title_fk
	FOREIGN KEY (title_id) REFERENCES wf_title(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_appointment_title_id_index ON wf_appointment (title_id);

ALTER TABLE ONLY wf_appointment ADD CONSTRAINT wf_appointment_position_fk
	FOREIGN KEY (position_id) REFERENCES wf_position(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_appointment_position_id_index ON wf_appointment (position_id);

ALTER TABLE ONLY wf_appointment ADD CONSTRAINT wf_appointment_appointment_status_fk
	FOREIGN KEY (appointment_status_id) REFERENCES wf_appointment_status(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_appointment_appointment_status_id_index ON wf_appointment (appointment_status_id);

CREATE INDEX wf_appointment_start_date_index ON wf_appointment (start_date);
CREATE INDEX wf_appointment_end_date_index ON wf_appointment (end_date);
CREATE INDEX wf_appointment_created_index ON wf_appointment (created);


CREATE TABLE wf_job_action_type
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	active BOOLEAN NOT NULL
	);
ALTER TABLE wf_job_action_type ADD CONSTRAINT wf_job_action_type_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_job_action_type_code_index ON wf_job_action_type (code);


CREATE TABLE wf_workflow
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	job_action_type_id INT NOT NULL
	);
ALTER TABLE wf_workflow ADD CONSTRAINT wf_workflow_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_workflow_code_index ON wf_workflow (code);
ALTER TABLE ONLY wf_workflow ADD CONSTRAINT wf_workflow_wf_job_action_type_fk
	FOREIGN KEY (job_action_type_id) REFERENCES wf_job_action_type(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_workflow_metatrack
	(id SERIAL,
	workflow_id INT NOT NULL,
	metatrack_id INT NOT NULL
	);
ALTER TABLE wf_workflow_metatrack ADD CONSTRAINT wf_workflow_metatrack_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_workflow_metatrack ADD CONSTRAINT wf_workflow_metatrack_wf_workflow_fk
	FOREIGN KEY (workflow_id) REFERENCES wf_workflow(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_workflow_metatrack ADD CONSTRAINT wf_workflow_metatrack_wf_metatrack_fk
	FOREIGN KEY (metatrack_id) REFERENCES wf_metatrack(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_job_action
	(id SERIAL,
	person_id INT,
	position_id INT NOT NULL,
	appointment_id INT NOT NULL,
	primary_job_action_id INT,
	job_action_type_id INT NOT NULL,
	current_status VARCHAR NOT NULL,
	workflow_id INT NOT NULL,
	workflow_json VARCHAR NOT NULL,
	complete BOOLEAN  NOT NULL,
	frozen BOOLEAN NOT NULL,
	revisions_required BOOLEAN NOT NULL,
	field_revisions_required BOOLEAN NOT NULL,
	cancelation_comment VARCHAR NOT NULL,
	cancelation_user VARCHAR NOT NULL,
	cancelation_date VARCHAR NOT NULL,
	proposed_start_date VARCHAR NOT NULL,
	external_key VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	completed VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_job_action ADD CONSTRAINT wf_job_action_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_job_action ADD CONSTRAINT wf_job_action_person_fk
	FOREIGN KEY (person_id) REFERENCES wf_person(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_job_action_person_id_index ON wf_job_action (person_id);

ALTER TABLE ONLY wf_job_action ADD CONSTRAINT wf_job_action_position_fk
	FOREIGN KEY (position_id) REFERENCES wf_position(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_job_action_position_id_index ON wf_job_action (position_id);

ALTER TABLE ONLY wf_job_action ADD CONSTRAINT wf_job_action_appointment_fk
	FOREIGN KEY (appointment_id) REFERENCES wf_appointment(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_job_action_appointment_id_index ON wf_job_action (appointment_id);

ALTER TABLE ONLY wf_job_action ADD CONSTRAINT wf_job_action_workflow_fk
	FOREIGN KEY (workflow_id) REFERENCES wf_workflow(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_job_action_workflow_id_index ON wf_job_action (workflow_id);

ALTER TABLE ONLY wf_job_action ADD CONSTRAINT wf_job_action_primary_job_action_fk
	FOREIGN KEY (primary_job_action_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY wf_job_action ADD CONSTRAINT wf_job_action_wf_job_action_type_fk
	FOREIGN KEY (job_action_type_id) REFERENCES wf_job_action_type(id) DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX wf_job_action_completed_index ON wf_job_action (completed);
CREATE UNIQUE INDEX wf_job_action_external_key_index ON wf_job_action (external_key);


CREATE TABLE wf_job_task
	(id SERIAL,
	job_action_id INT NOT NULL,
	task_code VARCHAR NOT NULL,
	primary_job_task_id INT NULL,
	frozen BOOLEAN NOT NULL,
	revisions_required_approval_task VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_job_task ADD CONSTRAINT wf_job_task_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_job_task ADD CONSTRAINT wf_job_task_job_action_fk
	FOREIGN KEY (job_action_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_job_task ADD CONSTRAINT wf_job_task_primary_job_task_fk
	FOREIGN KEY (primary_job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX wf_job_task_job_action_id_task_code_index ON wf_job_task (job_action_id,task_code);
CREATE INDEX wf_job_task_primary_job_task_id_index ON wf_job_task (primary_job_task_id);


CREATE TABLE wf_job_action_log
	(id SERIAL,
	job_action_id INT NOT NULL,
	job_task_id INT NOT NULL,
	class_name VARCHAR NOT NULL,
	verb VARCHAR NOT NULL,
	item VARCHAR NOT NULL,
	message VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_job_action_log ADD CONSTRAINT wf_job_action_log_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_job_action_log ADD CONSTRAINT wf_job_action_log_job_action_fk
	FOREIGN KEY (job_action_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_job_action_log_job_action_id_index ON wf_job_action_log (job_action_id);

ALTER TABLE ONLY wf_job_action_log ADD CONSTRAINT wf_job_action_log_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_job_action_log_job_task_id_index ON wf_job_action_log (job_task_id);


CREATE TABLE wf_activity_log
	(id SERIAL,
	job_action_id INT NOT NULL,
	job_task_id INT NOT NULL,
	activity VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_activity_log ADD CONSTRAINT wf_activity_log_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_activity_log ADD CONSTRAINT wf_activity_log_job_action_fk
	FOREIGN KEY (job_action_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_activity_log_job_action_id_index ON wf_activity_log (job_action_id);

ALTER TABLE ONLY wf_activity_log ADD CONSTRAINT wf_activity_log_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_activity_log_job_task_id_index ON wf_activity_log (job_task_id);


CREATE TABLE wf_comment
	(id SERIAL,
	activity_log_id INT NOT NULL,
	comment_code VARCHAR NOT NULL,
	comment VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_comment ADD CONSTRAINT wf_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_comment ADD CONSTRAINT wf_comment_wf_activity_log_fk
	FOREIGN KEY (activity_log_id) REFERENCES wf_activity_log(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_comment_wf_activity_log_id_index ON wf_comment (activity_log_id);



CREATE TABLE wf_file_repo
	(id SERIAL,
	job_task_id INT NOT NULL,
	seq_nbr INT NOT NULL,
	version_nbr INT NOT NULL,
	deleted boolean NOT NULL,
	file_name VARCHAR NOT NULL,
	pdf_version_nbr VARCHAR NOT NULL,
	pages INT NOT NULL,
	content bytea NOT NULL,
	content_type VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_file_repo ADD CONSTRAINT wf_file_repo_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_file_repo ADD CONSTRAINT wf_file_repo_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX wf_file_repo_job_task_id_seq_nbr_version_nbr_index ON wf_file_repo (job_task_id,seq_nbr,version_nbr);


CREATE TABLE wf_approval
	(id SERIAL,
	job_task_id INT NOT NULL,
	approval VARCHAR NOT NULL,
	approval_date VARCHAR NOT NULL,
	vote_for INT NOT NULL,
	vote_against INT NOT NULL,
	vote_abstain INT NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_approval ADD CONSTRAINT wf_approval_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_approval ADD CONSTRAINT wf_approval_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX wf_approval_job_task_id_index ON wf_approval (job_task_id);


CREATE TABLE wf_completion
	(id SERIAL,
	job_task_id INT NOT NULL,
	termination_type_id INT,
	effective_date VARCHAR NOT NULL,
	scheduled_date VARCHAR NOT NULL,
	complete BOOLEAN  NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_completion ADD CONSTRAINT wf_completion_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_completion ADD CONSTRAINT wf_completion_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX wf_completion_job_task_id_index ON wf_completion (job_task_id);
ALTER TABLE ONLY wf_completion ADD CONSTRAINT wf_completion_termination_type_fk
	FOREIGN KEY (termination_type_id) REFERENCES wf_termination_type(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_placeholder
	(id SERIAL,
	job_task_id INT NOT NULL,
	complete BOOLEAN  NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_placeholder ADD CONSTRAINT wf_placeholder_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_placeholder ADD CONSTRAINT wf_placeholder_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX wf_placeholder_job_task_id_index ON wf_placeholder (job_task_id);


CREATE TABLE wf_component_type
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL
	);
ALTER TABLE wf_component_type ADD CONSTRAINT wf_component_type_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_component_type_code_index ON wf_component_type (code);


CREATE TABLE wf_component
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	component_type_id INT NOT NULL,
	is_site_override boolean NOT NULL,
	value VARCHAR NOT NULL,
	src VARCHAR NOT NULL,
	car_relative_path VARCHAR NOT NULL
	);
ALTER TABLE wf_component ADD CONSTRAINT wf_component_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_component_code_index ON wf_component (code);
CREATE INDEX wf_component_is_site_override_index ON wf_component (is_site_override);
ALTER TABLE ONLY wf_component ADD CONSTRAINT wf_component_wf_component_type_fk
	FOREIGN KEY (component_type_id) REFERENCES wf_component_type(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_component_component_type_id_index ON wf_component (component_type_id);


CREATE TABLE wf_component_override
	(id SERIAL,
	workflow_code VARCHAR NOT NULL,
	component_code VARCHAR NOT NULL,
	title_code VARCHAR NOT NULL,
	value VARCHAR NOT NULL
	);
ALTER TABLE wf_component_override ADD CONSTRAINT wf_component_override_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_component_override_workflow_code_component_code_title_code_index ON wf_component_override (workflow_code,component_code,title_code);


CREATE TABLE wf_packet
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL
	);
ALTER TABLE wf_packet ADD CONSTRAINT wf_packet_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_packet_code_index ON wf_packet (code);


CREATE TABLE wf_packet_group
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	seq INT NOT NULL,
	packet_id INT NOT NULL
	);
ALTER TABLE wf_packet_group ADD CONSTRAINT wf_packet_group_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_packet_group ADD CONSTRAINT wf_packet_group_wf_packet_id_fk
	FOREIGN KEY (packet_id) REFERENCES wf_packet(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_packet_group_packet_id_index ON wf_packet_group (packet_id);
CREATE UNIQUE INDEX wf_packet_group_code_packet_id_index ON wf_packet_group (code,packet_id);


CREATE TABLE wf_packet_item
	(id SERIAL,
	item_code VARCHAR NOT NULL,
	seq INT NOT NULL,
	packet_group_id INT NOT NULL,
	is_artifact boolean NOT NULL,
	artifact_config_dict VARCHAR NOT NULL
	);
ALTER TABLE wf_packet_item ADD CONSTRAINT wf_packet_item_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_packet_item ADD CONSTRAINT wf_packet_item_wf_packet_group_id_fk
	FOREIGN KEY (packet_group_id) REFERENCES wf_packet_group(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_packet_item_packet_group_id_index ON wf_packet_item (packet_group_id);
CREATE INDEX wf_packet_item_item_code_index ON wf_packet_item (item_code);


CREATE TABLE wf_email
	(id SERIAL,
	job_action_id INT NOT NULL,
	task_code VARCHAR NOT NULL,
	email_from VARCHAR NOT NULL,
	email_to VARCHAR NOT NULL,
	email_cc VARCHAR NOT NULL,
	email_bcc VARCHAR NOT NULL,
	email_subject VARCHAR NOT NULL,
	email_body VARCHAR NOT NULL,
	email_date VARCHAR NOT NULL,
	email_sent boolean NOT NULL,
	email_send_response VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_email ADD CONSTRAINT wf_email_id PRIMARY KEY (id);
CREATE INDEX wf_email_email_to_index ON wf_email (email_to);
CREATE INDEX wf_email_task_code_index ON wf_email (task_code);
ALTER TABLE ONLY wf_email ADD CONSTRAINT wf_email_job_action_fk
	FOREIGN KEY (job_action_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_email_job_action_id_index ON wf_email (job_action_id);


CREATE TABLE wf_email_attachment
	(id SERIAL,
	email_id INT NOT NULL,
	descr VARCHAR,
	attachment bytea NOT NULL
	);
ALTER TABLE wf_email_attachment ADD CONSTRAINT wf_email_attachment_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_email_attachment ADD CONSTRAINT wf_email_attachment_email_fk
	FOREIGN KEY (email_id) REFERENCES wf_email(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_email_attachment_email_id_index ON wf_email_attachment (email_id);


CREATE TABLE wf_dashboard
	(id SERIAL,
	code VARCHAR NOT NULL,
	description VARCHAR NOT NULL,
	active boolean NOT NULL,
	job_action_id INT NOT NULL,
	department_id INT NOT NULL,
	view_permission VARCHAR NOT NULL,
	sort_order VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_dashboard ADD CONSTRAINT wf_dashboard_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_dashboard ADD CONSTRAINT wf_dashboard_job_action_fk
	FOREIGN KEY (job_action_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_dashboard_job_action_id_index ON wf_dashboard (job_action_id);

ALTER TABLE ONLY wf_dashboard ADD CONSTRAINT wf_dashboard_department_fk
	FOREIGN KEY (department_id) REFERENCES wf_department(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_dashboard_department_id_index ON wf_dashboard (department_id);

CREATE INDEX wf_dashboard_active_index ON wf_dashboard (active);


CREATE TABLE wf_question
	(id SERIAL,
	task_code varchar NOT NULL,
	code varchar NOT NULL,
	prompt varchar NOT NULL,
	required boolean NOT NULL,
	seq INT NOT NULL,
	active boolean NOT NULL,
	identifier_code VARCHAR NOT NULL,
	nbr_rows INT NOT NULL
	);
ALTER TABLE wf_question ADD CONSTRAINT wf_question_id PRIMARY KEY (id);
CREATE INDEX wf_question_task_code_index ON wf_question (task_code);
CREATE UNIQUE INDEX wf_question_code_index ON wf_question (code);
CREATE INDEX wf_question_seq_index ON wf_question (seq);
CREATE INDEX wf_question_active_index ON wf_question (active);


CREATE TABLE wf_question_option
	(id SERIAL,
	question_id INT NOT NULL,
	code varchar NOT NULL,
	option_text varchar NOT NULL,
	has_text boolean NOT NULL,
	text_title varchar NOT NULL,
	text_required boolean NOT NULL,
	seq INT NOT NULL,
	active boolean NOT NULL,
	nbr_rows INT NOT NULL
	);
ALTER TABLE wf_question_option ADD CONSTRAINT wf_question_option_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_question_option_code_index ON wf_question_option (code);
CREATE INDEX wf_question_option_seq_index ON wf_question_option (seq);
CREATE INDEX wf_question_option_question_id_index ON wf_question_option (question_id);
ALTER TABLE ONLY wf_question_option ADD CONSTRAINT wf_question_option_question_id_fk
	FOREIGN KEY (question_id) REFERENCES wf_question(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_question_response
	(id SERIAL,
	job_task_id INT NOT NULL,
	text_response VARCHAR NOT NULL,
	question_id INT NOT NULL,
	question_option_id INT,
	complete boolean NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_question_response ADD CONSTRAINT wf_question_response_id PRIMARY KEY (id);
CREATE INDEX wf_question_response_question_id_index ON wf_question_response (question_id);
CREATE INDEX wf_question_response_question_option_id_index ON wf_question_response (question_option_id);
ALTER TABLE ONLY wf_question_response ADD CONSTRAINT wf_question_response_question_id_fk
	FOREIGN KEY (question_id) REFERENCES wf_question(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_question_response ADD CONSTRAINT wf_question_response_question_option_id_fk
	FOREIGN KEY (question_id) REFERENCES wf_question_option(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_question_response ADD CONSTRAINT wf_question_response_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_question_response_job_task_id_index ON wf_question_response (job_task_id);


CREATE TABLE wf_evaluator_type
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	is_external boolean NOT NULL,
	is_arms_length boolean NOT NULL,
	requires_approval boolean NOT NULL
	);
ALTER TABLE wf_evaluator_type ADD CONSTRAINT wf_evaluator_type_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_evaluator_type_code_index ON wf_evaluator_type (code);


CREATE TABLE wf_evaluator_source
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL
	);
ALTER TABLE wf_evaluator_source ADD CONSTRAINT wf_evaluator_source_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_evaluator_source_code_index ON wf_evaluator_source (code);


CREATE TABLE wf_evaluator
	(id SERIAL,
	job_task_id INT NOT NULL,

	--  Evaluator demographics.
	evaluator_source_id INT NULL,
	evaluator_type_id INT NULL,
	first_name VARCHAR NOT NULL,
	middle_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	suffix VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
	phone VARCHAR NOT NULL,
	salutation VARCHAR NOT NULL,
	degree VARCHAR NOT NULL,
	titles VARCHAR NOT NULL,
	institution VARCHAR NOT NULL,
	address_lines VARCHAR NOT NULL,
	city VARCHAR NOT NULL,
	state VARCHAR NOT NULL,
	postal VARCHAR NOT NULL,
	country VARCHAR NOT NULL,
	admission_date VARCHAR NOT NULL,
	program VARCHAR NOT NULL,

	reason VARCHAR NOT NULL,

	--  Solicitation email.
	emailed BOOLEAN NOT NULL,
	emailed_date VARCHAR NOT NULL,
	emailed_username VARCHAR NOT NULL,
	emailed_due_date VARCHAR NOT NULL,
	emailed_key VARCHAR NOT NULL,
	emailed_email_id INT,

	--  Arm's Length (or other) approval.
	approved BOOLEAN NOT NULL,
	approved_date VARCHAR NOT NULL,
	approved_username VARCHAR NOT NULL,
	approved_comment VARCHAR NOT NULL,

	--  Evaluation upload.
	uploaded BOOLEAN NOT NULL,
	uploaded_date VARCHAR NOT NULL,
	uploaded_username VARCHAR NOT NULL,
	uploaded_comment VARCHAR NOT NULL,
	uploaded_file_repo_seq_nbr INT NOT NULL,

	--  Evaluator declines.
	declined BOOLEAN NOT NULL,
	declined_date VARCHAR NOT NULL,
	declined_username VARCHAR NOT NULL,
	declined_comment VARCHAR NOT NULL,

	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_evaluator ADD CONSTRAINT wf_evaluator_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_evaluator ADD CONSTRAINT wf_evaluator_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_evaluator_job_task_id_index ON wf_evaluator (job_task_id);
CREATE INDEX wf_evaluator_emailed_key_index ON wf_evaluator (emailed_key);

ALTER TABLE ONLY wf_evaluator ADD CONSTRAINT wf_evaluator_wf_evaluator_source_fk
	FOREIGN KEY (evaluator_source_id) REFERENCES wf_evaluator_source(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_evaluator ADD CONSTRAINT wf_evaluator_wf_evaluator_type_fk
	FOREIGN KEY (evaluator_type_id) REFERENCES wf_evaluator_type(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_evaluator ADD CONSTRAINT wf_evaluator_wf_email_fk
	FOREIGN KEY (emailed_email_id) REFERENCES wf_email(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_confirmed_title
	(id SERIAL,
	job_task_id INT NOT NULL,
	title_id INT NOT NULL,
	department_id INT,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_confirmed_title ADD CONSTRAINT wf_confirmed_title_id PRIMARY KEY (id);
CREATE INDEX wf_confirmed_title_title_index ON wf_confirmed_title (title_id);
CREATE INDEX wf_confirmed_title_job_task_index ON wf_confirmed_title (job_task_id);

ALTER TABLE ONLY wf_confirmed_title ADD CONSTRAINT wf_confirmed_title_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_confirmed_title ADD CONSTRAINT wf_confirmed_title_title_fk
	FOREIGN KEY (title_id) REFERENCES wf_title(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_confirmed_title ADD CONSTRAINT wf_confirmed_title_department_fk
	FOREIGN KEY (department_id) REFERENCES wf_department(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_job_posting
	(id SERIAL,
	job_task_id INT NOT NULL,
	date_posted VARCHAR NOT NULL,
	posting_number VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_job_posting ADD CONSTRAINT wf_job_posting_id PRIMARY KEY (id);
CREATE INDEX wf_job_posting_job_task_index ON wf_job_posting (job_task_id);

ALTER TABLE ONLY wf_job_posting ADD CONSTRAINT wf_job_posting_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_attest
	(id SERIAL,
	job_task_id INT NOT NULL,
	complete BOOLEAN NOT NULL,
	attestor_name VARCHAR NOT NULL,
	attestor_department VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_attest ADD CONSTRAINT wf_attest_id PRIMARY KEY (id);
CREATE INDEX wf_attest_job_task_index ON wf_attest (job_task_id);

ALTER TABLE ONLY wf_attest ADD CONSTRAINT wf_attest_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_npi
	(id SERIAL,
	job_task_id INT NOT NULL,
	npi_nbr VARCHAR NOT NULL,
	does_not_have_npi BOOLEAN NOT NULL,
	npi_username VARCHAR NOT NULL,
	npi_password VARCHAR NOT NULL,
	agree BOOLEAN NOT NULL,
	complete BOOLEAN NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_npi ADD CONSTRAINT wf_npi_id PRIMARY KEY (id);
CREATE INDEX wf_npi_job_task_index ON wf_npi (job_task_id);

ALTER TABLE ONLY wf_npi ADD CONSTRAINT wf_npi_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_disclosure
	(id SERIAL,
	job_task_id INT NOT NULL,
	has_disclosures BOOLEAN NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_disclosure ADD CONSTRAINT wf_disclosure_id PRIMARY KEY (id);
CREATE INDEX wf_disclosure_job_task_index ON wf_disclosure (job_task_id);

ALTER TABLE ONLY wf_disclosure ADD CONSTRAINT wf_disclosure_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_offense
	(id SERIAL,
	disclosure_id INT NOT NULL,
	offense_nbr INT NOT NULL,
	offense_key VARCHAR NOT NULL,
	offense_value VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_offense ADD CONSTRAINT wf_offense_id PRIMARY KEY (id);
CREATE INDEX wf_offense_disclosure_index ON wf_offense (disclosure_id);

ALTER TABLE ONLY wf_offense ADD CONSTRAINT wf_offense_disclosure_fk
	FOREIGN KEY (disclosure_id) REFERENCES wf_disclosure(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_background_check
	(id SERIAL,
	job_task_id INT NOT NULL,
	external_key VARCHAR NOT NULL,
	submitted_date VARCHAR NOT NULL,
	submitted_error VARCHAR NOT NULL,
	status VARCHAR NOT NULL,
	status_date VARCHAR NOT NULL,
	flagged BOOLEAN NOT NULL,
	report_url VARCHAR NOT NULL,
	report_content BYTEA NULL,
	completed_date VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_background_check ADD CONSTRAINT wf_background_check_id PRIMARY KEY (id);
CREATE INDEX wf_background_check_job_task_index ON wf_background_check (job_task_id);
CREATE INDEX wf_background_check_status_index ON wf_background_check (status);

ALTER TABLE ONLY wf_background_check ADD CONSTRAINT wf_background_check_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_credential_check_sequence
	(id SERIAL,
	seq INT NOT NULL
	);
ALTER TABLE wf_credential_check_sequence ADD CONSTRAINT wf_credential_check_sequence_id PRIMARY KEY (id);


CREATE TABLE oracle
	(id SERIAL,
	data varchar NOT NULL
	);
ALTER TABLE oracle ADD CONSTRAINT oracle_id PRIMARY KEY (id);
CREATE INDEX wf_oracle_data_index ON oracle (data);


--  Uber Forms
--
--  The following tables are used to define the prompts which appear on a Uber Form:
--      wf_uber_question    a question, the basic unit
--      wf_uber_option      allowable responses for certain types of questions
--      wf_uber_group       arbitrary groups of questions

CREATE TABLE wf_uber_question
	(id SERIAL,
	code varchar NOT NULL,
	descr VARCHAR NOT NULL,
	display_text VARCHAR NOT NULL,
	header_text VARCHAR NOT NULL,
	cols_offset INT NOT NULL,
	cols_label INT NOT NULL,
	cols_prompt INT NOT NULL,
	required boolean NOT NULL,
	wrap boolean NOT NULL,
	encrypt boolean NOT NULL,
	data_type VARCHAR NOT NULL,
	data_type_attributes varchar NOT NULL,
	job_action_types VARCHAR NOT NULL,
	identifier_code VARCHAR NOT NULL,
	show_codes VARCHAR NOT NULL,
	hide_codes VARCHAR NOT NULL
	);
ALTER TABLE wf_uber_question ADD CONSTRAINT wf_user_question_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_uber_question_code_index ON wf_uber_question (code);


CREATE TABLE wf_uber_option
	(id SERIAL,
	uber_question_id INT NOT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	display_text VARCHAR NOT NULL,
	seq INT NOT NULL,
	show_codes VARCHAR NOT NULL,
	hide_codes VARCHAR NOT NULL
	);
ALTER TABLE wf_uber_option ADD CONSTRAINT wf_uber_option_id PRIMARY KEY (id);
CREATE INDEX wf_uber_option_uber_question_id_index ON wf_uber_option (uber_question_id);
CREATE UNIQUE INDEX wf_uber_option_code_index ON wf_uber_option (code);
CREATE INDEX wf_uber_option_seq_index ON wf_uber_option (seq);
ALTER TABLE ONLY wf_uber_option ADD CONSTRAINT wf_uber_option_uber_question_id_fk
	FOREIGN KEY (uber_question_id) REFERENCES wf_uber_question(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_uber_group
	(id SERIAL,
	code varchar NOT NULL,
	descr VARCHAR NOT NULL,
	display_text VARCHAR NOT NULL,
	cols_offset INT NOT NULL,
	cols_label INT NOT NULL,
	repeating boolean NOT NULL,
	repeating_table boolean NOT NULL,
	required boolean NOT NULL,
	wrap boolean NOT NULL,
	filler boolean NOT NULL,
	children VARCHAR NOT NULL
	);
ALTER TABLE wf_uber_group ADD CONSTRAINT wf_uber_group_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_uber_group_code_index ON wf_uber_group (code);


--  The following tables hold responses for a specific uber form instance:
--      wf_uber             json representation of questions for a specific uber form instance
--      wf_uber_response    responses to individual questions

CREATE TABLE wf_uber
	(id SERIAL,
	job_task_id INT NOT NULL,
	uber_question_json VARCHAR NOT NULL,
	complete boolean NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_uber ADD CONSTRAINT wf_uber_id PRIMARY KEY (id);
CREATE INDEX wf_uber_job_task_id_index ON wf_uber (job_task_id);
ALTER TABLE ONLY wf_uber ADD CONSTRAINT wf_uber_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_uber_response
	(id SERIAL,
	job_task_id INT NOT NULL,
	question_code VARCHAR NOT NULL,
	repeat_seq INT NOT NULL,
	response VARCHAR NOT NULL,
	revisions_required boolean NOT NULL,
	revisions_required_date VARCHAR NOT NULL,
	revisions_required_comment VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_uber_response ADD CONSTRAINT wf_uber_response_id PRIMARY KEY (id);
CREATE INDEX wf_uber_response_job_task_id_index ON wf_uber_response (job_task_id);
CREATE INDEX wf_uber_response_question_code_index ON wf_uber_response (question_code);
ALTER TABLE ONLY wf_uber_response ADD CONSTRAINT wf_uber_response_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;


--  The following tables support uber form saved sets:
--      wf_uber_saved_set         a named collection of wf_uber_saved_set_item records
--      wf_uber_saved_set_item    responses to individual questions

CREATE TABLE wf_uber_saved_set
	(id SERIAL,
	community VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	group_code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_uber_saved_set ADD CONSTRAINT wf_uber_saved_set_id PRIMARY KEY (id);
CREATE INDEX wf_uber_saved_set_community_index ON wf_uber_saved_set (community);
CREATE INDEX wf_uber_saved_set_username_index ON wf_uber_saved_set (username);
CREATE INDEX wf_uber_saved_set_group_code_index ON wf_uber_saved_set (group_code);


CREATE TABLE wf_uber_saved_set_item
	(id SERIAL,
	saved_set_id INT NOT NULL,
	question_code VARCHAR NOT NULL,
	repeat_seq INT NOT NULL,
	response VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_uber_saved_set_item ADD CONSTRAINT wf_uber_saved_set_item_id PRIMARY KEY (id);
CREATE INDEX wf_uber_saved_set_item_saved_set_id_index ON wf_uber_saved_set_item (saved_set_id);
ALTER TABLE ONLY wf_uber_saved_set_item ADD CONSTRAINT wf_uber_saved_set_item_saved_set_fk
	FOREIGN KEY (saved_set_id) REFERENCES wf_uber_saved_set(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_permission_override
	(id SERIAL,
	job_action_id INT NOT NULL,
	job_task_code VARCHAR NOT NULL,
	department_id INT NOT NULL,
	access_allowed BOOLEAN NOT NULL
	);
ALTER TABLE wf_permission_override ADD CONSTRAINT wf_permission_override_id PRIMARY KEY (id);
CREATE INDEX wf_permission_override_job_action_id_index ON wf_permission_override (job_action_id);
CREATE INDEX wf_permission_override_department_id_index ON wf_permission_override (department_id);
CREATE INDEX wf_permission_override_access_allowed_index ON wf_permission_override (access_allowed);

ALTER TABLE ONLY wf_permission_override ADD CONSTRAINT wf_permission_override_job_action_fk
	FOREIGN KEY (job_action_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY wf_permission_override ADD CONSTRAINT wf_permission_override_department_fk
	FOREIGN KEY (department_id) REFERENCES wf_department(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_item_injection
	(id SERIAL,
	job_task_id INT NOT NULL,
	task_codes VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_item_injection ADD CONSTRAINT wf_item_injection_id PRIMARY KEY (id);
CREATE INDEX wf_item_injection_job_task_id_index ON wf_item_injection (job_task_id);
ALTER TABLE ONLY wf_item_injection ADD CONSTRAINT wf_item_injection_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_joint_promotion
	(id SERIAL,
	job_task_id INT NOT NULL,
	title_id INT NOT NULL,
	position_id INT NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_joint_promotion ADD CONSTRAINT wf_joint_promotion_id PRIMARY KEY (id);
CREATE INDEX wf_joint_promotion_job_task_id_index ON wf_joint_promotion (job_task_id);
ALTER TABLE ONLY wf_joint_promotion ADD CONSTRAINT wf_joint_promotion_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_joint_promotion_title_id_index ON wf_joint_promotion (title_id);
ALTER TABLE ONLY wf_joint_promotion ADD CONSTRAINT wf_joint_promotion_title_fk
	FOREIGN KEY (title_id) REFERENCES wf_title(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_joint_promotion_position_id_index ON wf_joint_promotion (position_id);
ALTER TABLE ONLY wf_joint_promotion ADD CONSTRAINT wf_joint_promotion_position_fk
	FOREIGN KEY (position_id) REFERENCES wf_position(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE wf_track_change
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	workflow_code VARCHAR NOT NULL
	);
ALTER TABLE wf_track_change ADD CONSTRAINT wf_track_change_id PRIMARY KEY (id);
CREATE UNIQUE INDEX wf_track_change_code_index ON wf_track_change (code);


CREATE TABLE wf_track_change_map
	(id SERIAL,
	track_change_id INT NOT NULL,
	from_track_id INT NOT NULL,
	to_track_id INT NOT NULL,
	from_title_id INT NOT NULL,
	to_title_id INT NOT NULL
	);
ALTER TABLE wf_track_change_map ADD CONSTRAINT wf_track_change_map_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_track_change_map ADD CONSTRAINT wf_track_change_map_track_change_fk
	FOREIGN KEY (track_change_id) REFERENCES wf_track_change(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_track_change_map_track_change_id_index ON wf_track_change_map (track_change_id);
ALTER TABLE ONLY wf_track_change_map ADD CONSTRAINT wf_track_change_map_from_track_fk
	FOREIGN KEY (from_track_id) REFERENCES wf_track(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_track_change_map_from_track_id_index ON wf_track_change_map (from_track_id);
ALTER TABLE ONLY wf_track_change_map ADD CONSTRAINT wf_track_change_map_to_track_fk
	FOREIGN KEY (to_track_id) REFERENCES wf_track(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_track_change_map_to_track_id_index ON wf_track_change_map (to_track_id);
ALTER TABLE ONLY wf_track_change_map ADD CONSTRAINT wf_track_change_map_from_title_fk
	FOREIGN KEY (from_title_id) REFERENCES wf_title(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_track_change_map_from_title_id_index ON wf_track_change_map (from_title_id);
ALTER TABLE ONLY wf_track_change_map ADD CONSTRAINT wf_track_change_map_to_title_fk
	FOREIGN KEY (to_title_id) REFERENCES wf_title(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_track_change_map_to_title_id_index ON wf_track_change_map (to_title_id);


CREATE TABLE wf_reporting
	(id SERIAL,
	community VARCHAR NOT NULL,
	username VARCHAR NOT NULL,
	report_name VARCHAR NOT NULL,
	src_file VARCHAR NOT NULL,
	parameters VARCHAR NOT NULL,
	content bytea NOT NULL,
	date_created VARCHAR NOT NULL,
	file_type VARCHAR NOT NULL,
	date_read VARCHAR NOT NULL
	);
ALTER TABLE wf_reporting ADD CONSTRAINT wf_reporting_id PRIMARY KEY (id);
CREATE INDEX wf_reporting_community_index ON wf_reporting (community);
CREATE INDEX wf_reporting_username_index ON wf_reporting (username);
CREATE INDEX wf_reporting_report_name_index ON wf_reporting (report_name);
CREATE INDEX wf_reporting_date_created_index ON wf_reporting (date_created);


CREATE TABLE wf_related_job_actions
	(id SERIAL,
	job_action1_id INT NOT NULL,
	job_action2_id INT NOT NULL
	);
ALTER TABLE wf_related_job_actions ADD CONSTRAINT wf_related_job_actions_id PRIMARY KEY (id);
ALTER TABLE ONLY wf_related_job_actions ADD CONSTRAINT wf_related_job_actions_job_action1_fk
	FOREIGN KEY (job_action1_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_related_job_actions_job_action1_id_index ON wf_related_job_actions (job_action1_id);
ALTER TABLE ONLY wf_related_job_actions ADD CONSTRAINT wf_related_job_actions_job_action2_fk
	FOREIGN KEY (job_action2_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_related_job_actions_job_action2_id_index ON wf_related_job_actions (job_action2_id);


CREATE TABLE wf_building
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	active BOOLEAN NOT NULL,
	address_lines VARCHAR NOT NULL,
	city VARCHAR NOT NULL,
	state VARCHAR NOT NULL,
	country VARCHAR NOT NULL,
	postal VARCHAR NOT NULL
	);
ALTER TABLE wf_building ADD CONSTRAINT wf_building_id PRIMARY KEY (id);
CREATE INDEX wf_building_descr ON wf_building (descr);
CREATE UNIQUE INDEX wf_building_code ON wf_building (code);


CREATE TABLE wf_service_rank
	(id SERIAL,
	job_task_id INT NOT NULL,
	building_descr VARCHAR NOT NULL,
	room VARCHAR NOT NULL,
	spc VARCHAR NOT NULL,
	floor VARCHAR NOT NULL,
	reception VARCHAR NOT NULL,
	address_lines VARCHAR NOT NULL,
	city VARCHAR NOT NULL,
	state VARCHAR NOT NULL,
	country VARCHAR NOT NULL,
	postal VARCHAR NOT NULL,
	phone VARCHAR NOT NULL,
	fax VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
	membership_category VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_service_rank ADD CONSTRAINT wf_service_rank_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_service_rank ADD CONSTRAINT wf_service_rank_job_task_fk
	FOREIGN KEY (job_task_id) REFERENCES wf_job_task(id) DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX wf_service_rank_job_task_id_index ON wf_service_rank (job_task_id);


CREATE TABLE wf_field_revisions
	(id SERIAL,
	job_action_id INT NOT NULL,
	task_code VARCHAR NOT NULL,
	field_name VARCHAR NOT NULL,
	comment VARCHAR NOT NULL,
	complete BOOLEAN NOT NULL,
	who_requested VARCHAR NOT NULL,
	when_requested VARCHAR NOT NULL,
	who_notified VARCHAR NOT NULL,
	when_notified VARCHAR NOT NULL,
	who_resolved VARCHAR NOT NULL,
	when_resolved VARCHAR NOT NULL,
	created VARCHAR NOT NULL,
	updated VARCHAR NOT NULL,
	lastuser VARCHAR NOT NULL
	);
ALTER TABLE wf_field_revisions ADD CONSTRAINT wf_field_revisions_id PRIMARY KEY (id);

ALTER TABLE ONLY wf_field_revisions ADD CONSTRAINT wf_field_revisions_job_action_fk
	FOREIGN KEY (job_action_id) REFERENCES wf_job_action(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX wf_field_revisions_job_action_id_index ON wf_field_revisions (job_action_id);

CREATE INDEX wf_field_revisions_task_code ON wf_field_revisions (task_code);
CREATE INDEX wf_field_revisions_complete ON wf_field_revisions (complete);
CREATE INDEX wf_field_revisions_when_notified ON wf_field_revisions (when_notified);
CREATE INDEX wf_field_revisions_when_resolved ON wf_field_revisions (when_resolved);
CREATE INDEX wf_field_revisions_field_name ON wf_field_revisions (field_name);


CREATE TABLE wf_internal_evaluator
	(id SERIAL,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	email_address VARCHAR NOT NULL,
	active BOOLEAN NOT NULL
	);
ALTER TABLE wf_internal_evaluator ADD CONSTRAINT wf_internal_evaluator_id PRIMARY KEY (id);
