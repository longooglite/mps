SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

CREATE TABLE application
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	url VARCHAR NOT NULL);
ALTER TABLE application ADD CONSTRAINT application_id PRIMARY KEY (id);
CREATE UNIQUE INDEX application_code_index ON application (code);


CREATE TABLE site
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	active_start VARCHAR NULL,
	active_end VARCHAR NULL);
ALTER TABLE site ADD CONSTRAINT site_id PRIMARY KEY (id);
CREATE UNIQUE INDEX site_code_index ON site (code);


CREATE TABLE site_preference
	(id SERIAL,
	site_code VARCHAR NOT NULL,
	code VARCHAR NOT NULL,
	value TEXT NOT NULL);
ALTER TABLE site_preference ADD CONSTRAINT site_preference_id PRIMARY KEY (id);
CREATE UNIQUE INDEX site_preference_code_index ON site_preference (site_code, code);


CREATE TABLE site_application
	(id SERIAL,
	site_id INT NOT NULL,
	application_id INT NOT NULL);
ALTER TABLE site_application ADD CONSTRAINT site_application_id PRIMARY KEY (id);
CREATE UNIQUE INDEX site_application_site_application_index ON site_application (site_id, application_id);
ALTER TABLE ONLY site_application ADD CONSTRAINT site_application_site_fk
    FOREIGN KEY (site_id) REFERENCES site(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY site_application ADD CONSTRAINT site_application_application_fk
    FOREIGN KEY (application_id) REFERENCES application(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE site_community
	(id SERIAL,
	site_id INT NOT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL);
ALTER TABLE site_community ADD CONSTRAINT site_community_id PRIMARY KEY (id);
CREATE UNIQUE INDEX site_community_code_index ON site_community (site_id, code);

    
CREATE TABLE mpsuser
	(id SERIAL,
	site_id INT NOT NULL,
	community_id INT NOT NULL,
	username VARCHAR NOT NULL,
	password VARCHAR NOT NULL,
	first_name VARCHAR NOT NULL,
	last_name VARCHAR NOT NULL,
	email VARCHAR NOT NULL,
	auth_override VARCHAR NOT NULL,
	active BOOLEAN NOT NULL);
ALTER TABLE mpsuser ADD CONSTRAINT mpsuser_id PRIMARY KEY (id);
ALTER TABLE ONLY mpsuser ADD CONSTRAINT mpsuser_site_fk
    FOREIGN KEY (site_id) REFERENCES site(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY mpsuser ADD CONSTRAINT mpsuser_community_fk
    FOREIGN KEY (community_id) REFERENCES site_community(id) DEFERRABLE INITIALLY DEFERRED;
CREATE UNIQUE INDEX mpsuser_site_community_username_index ON mpsuser (site_id, community_id, username);


CREATE TABLE mpsuser_application
	(id SERIAL,
	mpsuser_id INT NOT NULL,
	application_id INT NOT NULL,
	seqnbr INT NOT NULL);
ALTER TABLE mpsuser_application ADD CONSTRAINT mpsuser_application_id PRIMARY KEY (id);
CREATE UNIQUE INDEX mpsuser_application_mpsuser_application_index ON mpsuser_application (mpsuser_id, application_id);
ALTER TABLE ONLY mpsuser_application ADD CONSTRAINT mpsuser_application_mpsuser_fk
    FOREIGN KEY (mpsuser_id) REFERENCES mpsuser(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY mpsuser_application ADD CONSTRAINT mpsuser_application_application_fk
    FOREIGN KEY (application_id) REFERENCES application(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE permission
	(id SERIAL,
	site_code VARCHAR NOT NULL,
	application_id INT NOT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL);
ALTER TABLE permission ADD CONSTRAINT permission_id PRIMARY KEY (id);
CREATE UNIQUE INDEX permission_site_application_code_index ON permission (site_code, application_id, code);
ALTER TABLE ONLY permission ADD CONSTRAINT permission_application_fk
    FOREIGN KEY (application_id) REFERENCES application(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE role
	(id SERIAL,
	site_id INT NOT NULL,
	application_id INT NOT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL);
ALTER TABLE role ADD CONSTRAINT role_id PRIMARY KEY (id);
CREATE UNIQUE INDEX role_site_application_code_index ON role (site_id, application_id, code);
ALTER TABLE ONLY role ADD CONSTRAINT role_site_fk
    FOREIGN KEY (site_id) REFERENCES site(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY role ADD CONSTRAINT role_application_fk
    FOREIGN KEY (application_id) REFERENCES application(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE role_permission
	(id SERIAL,
	role_id INT NOT NULL,
	permission_id INT NOT NULL);
ALTER TABLE role_permission ADD CONSTRAINT role_permission_id PRIMARY KEY (id);
CREATE UNIQUE INDEX role_permission_role_permission_index ON role_permission (role_id, permission_id);
ALTER TABLE ONLY role_permission ADD CONSTRAINT role_permission_role_fk
    FOREIGN KEY (role_id) REFERENCES role(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY role_permission ADD CONSTRAINT role_permission_permission_fk
    FOREIGN KEY (permission_id) REFERENCES permission(id) DEFERRABLE INITIALLY DEFERRED;


CREATE TABLE mpsuser_role
	(id SERIAL,
	mpsuser_id INT NOT NULL,
	role_id INT NOT NULL);
ALTER TABLE mpsuser_role ADD CONSTRAINT mpsuser_role_id PRIMARY KEY (id);
CREATE UNIQUE INDEX mpsuser_role_mpsuser_role_index ON mpsuser_role (mpsuser_id, role_id);
ALTER TABLE ONLY mpsuser_role ADD CONSTRAINT mpsuser_role_mpsuser_fk
    FOREIGN KEY (mpsuser_id) REFERENCES mpsuser(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY mpsuser_role ADD CONSTRAINT mpsuser_role_role_fk
    FOREIGN KEY (role_id) REFERENCES role(id) DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE access_log
	(id SERIAL,
	site VARCHAR,
	community VARCHAR,
	username VARCHAR,
	mpsid VARCHAR,
	access_action VARCHAR,
	created timestamp DEFAULT now()
	);
ALTER TABLE access_log ADD CONSTRAINT access_log_id PRIMARY KEY (id);
CREATE INDEX access_log_mpsid_index ON access_log (mpsid);

