import MPSCore.utilities.migrationFramework as MF

class Migrator(MF.MigrationHelper):
	def __init__(self,_connection):
		self.connection = _connection

	def migrate(self):
		try:
			if not self.tableExists(self.connection,"cv_selector_group"):
				sql = '''CREATE TABLE cv_selector_group
					    (id SERIAL,
						code VARCHAR NOT NULL,
						descr VARCHAR NOT NULL
						);
						ALTER TABLE cv_selector_group ADD CONSTRAINT cv_selector_group_id PRIMARY KEY (id);
						CREATE UNIQUE INDEX cv_selector_group_code_index ON cv_selector_group (code);'''
				self.connection.executeSQLCommand(sql,())
			if not self.tableExists(self.connection,"cv_selector"):
				sql = '''CREATE TABLE cv_selector
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
						    FOREIGN KEY (cv_selector_group_id) REFERENCES cv_selector_group(id) DEFERRABLE INITIALLY DEFERRED;'''
				self.connection.executeSQLCommand(sql,())
			return 0,''
		except Exception,e:
			self.connection.executeSQLCommand('rollback',())
			return -1,e.message
