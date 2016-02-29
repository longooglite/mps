SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

-- CV --

CREATE TABLE cv_static_lookup
	(id SERIAL,
	lookup_key VARCHAR NOT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	alt_descr VARCHAR NOT NULL,
	seq INT NOT NULL);
ALTER TABLE cv_static_lookup ADD CONSTRAINT cv_static_lookup_id PRIMARY KEY (id);
CREATE INDEX cv_static_lookup_seq_index ON cv_static_lookup (lookup_key,seq);
CREATE UNIQUE INDEX cv_static_lookup_lookup_key_code_index ON cv_static_lookup (lookup_key,code);
CREATE INDEX cv_static_lookup_code_index ON cv_static_lookup (code);

CREATE TABLE cv_affordance_type
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL);
ALTER TABLE cv_affordance_type ADD CONSTRAINT cv_affordance_type_id PRIMARY KEY (id);
CREATE INDEX cv_affordance_code_index ON cv_affordance_type (code);

CREATE TABLE cv_display_mode
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL);
ALTER TABLE cv_display_mode ADD CONSTRAINT cv_display_mode_id PRIMARY KEY (id);
CREATE INDEX cv_display_code_index ON cv_display_mode (code);

CREATE TABLE cv_proxy
	(id SERIAL,
	grantor_community VARCHAR NOT NULL,
	grantor VARCHAR NOT NULL,
	grantee_community VARCHAR NOT NULL,
	grantee VARCHAR NOT NULL,
	can_write boolean NOT NULL DEFAULT FALSE,
	accepted_when VARCHAR NOT NULL DEFAULT '',
	requested_when VARCHAR NOT NULL DEFAULT '',
	deleted_when VARCHAR NOT NULL DEFAULT '',
	deleted boolean NOT NULL default FALSE);
ALTER TABLE cv_proxy ADD CONSTRAINT cv_proxy_id PRIMARY KEY (id);
CREATE INDEX cv_proxy_community_grantor_index ON cv_proxy (grantor_community, grantor);
CREATE INDEX cv_proxy_community_grantee_index ON cv_proxy (grantee_community, grantee);
CREATE INDEX cv_proxy_deleted_index ON cv_proxy (deleted);

CREATE TABLE cv_person
	(id SERIAL,
	community VARCHAR NOT NULL,
	user_id VARCHAR NOT NULL,
	pubmedsearchkey VARCHAR NOT NULL DEFAULT '');
ALTER TABLE cv_person ADD CONSTRAINT cv_person_id PRIMARY KEY (id);
CREATE UNIQUE INDEX cv_person_community_user_id_index ON cv_person (community, user_id);

CREATE TABLE cv_row
	(id SERIAL,
	person_id INT NOT NULL,
	exclude_from_cv_val boolean DEFAULT FALSE NOT NULL,
	user_sort_seq INT DEFAULT 0 NOT NULL,
	who_dunit VARCHAR NOT NULL,
	when_dunit VARCHAR NOT NULL);
ALTER TABLE cv_row ADD CONSTRAINT cv_row_id PRIMARY KEY (id);
ALTER TABLE ONLY cv_row ADD CONSTRAINT cv_row_person_fk
    FOREIGN KEY (person_id) REFERENCES cv_person(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_row_person_index ON cv_row (person_id);

CREATE TABLE cv_category
	(id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	seq INT NOT NULL,
	parent_code VARCHAR NOT NULL DEFAULT '',
	exclude_from_cv_display boolean DEFAULT FALSE NOT NULL,
	display_options VARCHAR NOT NULL DEFAULT '',
	user_sortable boolean DEFAULT FALSE NOT NULL,
    list_display_mode_id INT NOT NULL,
    detail_display_mode_id INT NOT NULL,
    help_text VARCHAR NOT NULL DEFAULT '');
ALTER TABLE cv_category ADD CONSTRAINT cv_category_id PRIMARY KEY (id);
CREATE INDEX cv_category_code_index ON cv_category (code);
CREATE INDEX cv_category_parent_code_index ON cv_category (parent_code);
CREATE INDEX cv_category_seq_index ON cv_category (seq);
CREATE INDEX cv_category_list_display_mode_index ON cv_category (list_display_mode_id);
CREATE INDEX cv_category_detail_display_mode_index ON cv_category (detail_display_mode_id);
ALTER TABLE ONLY cv_category ADD CONSTRAINT cv_category_list_display_mode_fk
    FOREIGN KEY (list_display_mode_id) REFERENCES cv_display_mode(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY cv_category ADD CONSTRAINT cv_category_detail_display_mode_fk
    FOREIGN KEY (detail_display_mode_id) REFERENCES cv_display_mode(id) DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE cv_sub_category_group
	(id SERIAL,
    category_id INT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	seq INT NOT NULL);
ALTER TABLE cv_sub_category_group ADD CONSTRAINT cv_sub_category_group_id PRIMARY KEY (id);
CREATE INDEX cv_sub_category_group_code_index ON cv_sub_category_group (code);
CREATE INDEX cv_sub_category_group_seq_index ON cv_sub_category_group (seq);
ALTER TABLE ONLY cv_sub_category_group ADD CONSTRAINT cv_sub_category_group_category_fk
    FOREIGN KEY (category_id) REFERENCES cv_category(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_sub_category_group_category_index ON cv_sub_category_group (category_id);

CREATE TABLE cv_sub_category
	(id SERIAL,
	sub_category_group_id INT NOT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	seq INT NOT NULL);
ALTER TABLE cv_sub_category ADD CONSTRAINT cv_sub_category_id PRIMARY KEY (id);
CREATE INDEX cv_sub_category_code_index ON cv_sub_category (code);
ALTER TABLE ONLY cv_sub_category ADD CONSTRAINT cv_category_sub_category_group_fk
    FOREIGN KEY (sub_category_group_id) REFERENCES cv_sub_category_group(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_sub_category_sub_category_group_index ON cv_sub_category (sub_category_group_id);
CREATE INDEX cv_sub_category_seq_index ON cv_sub_category (seq);

CREATE TABLE cv_field_group
	(id SERIAL,
    category_id INT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	seq INT NOT NULL);
ALTER TABLE cv_field_group ADD CONSTRAINT cv_field_group_id PRIMARY KEY (id);
CREATE INDEX cv_field_group_code_index ON cv_field_group (code);
CREATE INDEX cv_field_group_seq_index ON cv_field_group (seq);
ALTER TABLE ONLY cv_field_group ADD CONSTRAINT cv_field_group_category_fk
    FOREIGN KEY (category_id) REFERENCES cv_category(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_field_group_category_index ON cv_field_group (category_id);

CREATE TABLE cv_field
	(id SERIAL,
	field_group_id INT NOT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	alt_descr VARCHAR NOT NULL,
	required boolean DEFAULT FALSE NOT NULL,
	seq INT NOT NULL,
	display_on_list_seq VARCHAR NOT NULL,
	display_on_pdf_seq VARCHAR NOT NULL,
	list_display_options VARCHAR NOT NULL,
	list_sort_key_seq INT NOT NULL,
    affordance_type_id INT NOT NULL,
    text_length INT NOT NULL DEFAULT 0,
	text_height INT NOT NULL DEFAULT 0,
	static_lookup_code VARCHAR NULL,
	date_format VARCHAR NOT NULL DEFAULT '',
	help_text VARCHAR NOT NULL DEFAULT '');
ALTER TABLE cv_field ADD CONSTRAINT cv_field_id PRIMARY KEY (id);
CREATE INDEX cv_field_seq_index ON cv_field (seq);
CREATE INDEX cv_field_display_on_list_seq_index ON cv_field (display_on_list_seq);
CREATE INDEX cv_field_display_on_pdf_seq_index ON cv_field (display_on_pdf_seq);
CREATE UNIQUE INDEX cv_field_code_index ON cv_field (code);
ALTER TABLE ONLY cv_field ADD CONSTRAINT cv_field_affordance_type_fk
    FOREIGN KEY (affordance_type_id) REFERENCES cv_affordance_type(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_field_affordance_type_index ON cv_field (affordance_type_id);
ALTER TABLE ONLY cv_field ADD CONSTRAINT cv_field_field_group_fk
    FOREIGN KEY (field_group_id) REFERENCES cv_field_group(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_field_field_group_index ON cv_field (field_group_id);

CREATE TABLE cv_attribute
	(id SERIAL,
	row_id INT NOT NULL,
	field_id INT NOT NULL,
	attribute_value TEXT NOT NULL DEFAULT '',
	who_dunit VARCHAR NOT NULL,
	when_dunit VARCHAR NOT NULL);
ALTER TABLE cv_attribute ADD CONSTRAINT cv_attribute_id PRIMARY KEY (id);
ALTER TABLE ONLY cv_attribute ADD CONSTRAINT cv_attribute_field_fk
    FOREIGN KEY (field_id) REFERENCES cv_field(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_attribute_field_index ON cv_attribute (field_id);

ALTER TABLE ONLY cv_attribute ADD CONSTRAINT cv_attribute_row_fk
    FOREIGN KEY (row_id) REFERENCES cv_row(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_attribute_row_index ON cv_attribute (row_id);

CREATE TABLE cv_publication_import
    (id SERIAL,
    person_id INT NOT NULL
    );
ALTER TABLE cv_publication_import ADD CONSTRAINT cv_publication_import_id PRIMARY KEY (id);
ALTER TABLE ONLY cv_publication_import ADD CONSTRAINT cv_publication_import_person_fk
    FOREIGN KEY (person_id) REFERENCES cv_person(id) DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE cv_pubmed_import
    (id SERIAL,
    publication_import_id INT NOT NULL,
    reviewed boolean NOT NULL DEFAULT FALSE,
    claimed boolean NOT NULL DEFAULT FALSE,
    entrywhen VARCHAR,
    authors VARCHAR,
    articleIds VARCHAR,
    attributes VARCHAR,
    languages VARCHAR,
    doccontriblist VARCHAR,
    pubType VARCHAR,
    reference VARCHAR,
    availablefromurl VARCHAR,
    bookname VARCHAR,
    booktitle VARCHAR,
    chapter VARCHAR,
    docdate DATE,
    doctype VARCHAR,
    edition VARCHAR,
    locationid VARCHAR,
    epubdate DATE,
    essn VARCHAR,
    fulljournalname VARCHAR,
    history VARCHAR,
    issn VARCHAR,
    issue VARCHAR,
    lastauthor VARCHAR,
    locationlabel VARCHAR,
    medium VARCHAR,
    nlmuniqueid VARCHAR,
    pages VARCHAR,
    pmcrefcount VARCHAR,
    publisherlocation VARCHAR,
    publishername VARCHAR,
    pubstatus VARCHAR,
    recordstatus VARCHAR,
    reportnumber VARCHAR,
    sortfirstauthor VARCHAR,
    sortpubdate VARCHAR,
    sorttitle VARCHAR,
    source VARCHAR,
    srcdate DATE,
    title VARCHAR,
    uid VARCHAR,
    vernaculartitle VARCHAR,
    viewcount VARCHAR,
    volume VARCHAR,
    authorSearchString VARCHAR,
    cvpublication_category VARCHAR
    );
ALTER TABLE cv_pubmed_import ADD CONSTRAINT cv_pubmed_import_id PRIMARY KEY (id);
ALTER TABLE ONLY cv_pubmed_import ADD CONSTRAINT cv_pubmed_import_pub_import_fk
    FOREIGN KEY (publication_import_id) REFERENCES cv_publication_import(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX cv_pubmed_import_publication_import_id_index ON cv_pubmed_import (publication_import_id);
CREATE INDEX cv_pubmed_import_uid_index ON cv_pubmed_import (uid);

CREATE TABLE cv_selector_group
    (id SERIAL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL
	);
ALTER TABLE cv_selector_group ADD CONSTRAINT cv_selector_group_id PRIMARY KEY (id);
CREATE UNIQUE INDEX cv_selector_group_code_index ON cv_selector_group (code);

CREATE TABLE cv_selector
    (id SERIAL,
    cv_selector_group_id INT NOT NULL,
	code VARCHAR NOT NULL,
	descr VARCHAR NOT NULL,
	seq INT NOT NULL,
	style VARCHAR NOT NULL
	);
ALTER TABLE cv_selector ADD CONSTRAINT cv_selector_id PRIMARY KEY (id);
CREATE UNIQUE INDEX cv_selector_code_index ON cv_selector (code);
ALTER TABLE ONLY cv_selector ADD CONSTRAINT cv_selector_cv_selector_group_fk
    FOREIGN KEY (cv_selector_group_id) REFERENCES cv_selector_group(id) DEFERRABLE INITIALLY DEFERRED;
