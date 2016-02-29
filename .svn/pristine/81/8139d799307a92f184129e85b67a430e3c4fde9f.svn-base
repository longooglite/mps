SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

-- Common --

CREATE TABLE migration_history
	(id SERIAL,
	created timestamp DEFAULT now(),
	migration VARCHAR,
	applied boolean
	);
ALTER TABLE migration_history ADD CONSTRAINT migration_history_id PRIMARY KEY (id);
CREATE UNIQUE INDEX migration_history_migration_index ON migration_history (migration);

