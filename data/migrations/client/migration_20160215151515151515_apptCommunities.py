import MPSCore.utilities.migrationFramework as MF

class Migrator(MF.MigrationHelper):
	def __init__(self,_connection):
		self.connection = _connection

	def migrate(self):
		try:
			if (self.tableExists(self.connection, 'wf_person')) and \
				(not self.columnExists(self.connection, 'wf_person', 'community')):

				for sql in self._getPersonStatements():
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				for sql in self._getDepartmentStatements():
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				for sql in self._getSavedSetStatements():
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				for sql in self._getReportingStatements():
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				self.connection.performCommit()

			return 0,""

		except Exception,e:
			self.connection.performRollback()
			return -1,e.message

	def _getPersonStatements(self):
		sql = []

		sql.append('''DROP INDEX IF EXISTS wf_person_username_index;''')
		sql.append('''ALTER TABLE wf_person ADD COLUMN community VARCHAR NULL;''')
		sql.append('''UPDATE wf_person SET community = 'default';''')
		sql.append('''ALTER TABLE wf_person ALTER COLUMN community SET NOT NULL;''')
		sql.append('''CREATE INDEX wf_person_community_username_index ON wf_person (community, username);''')

		return sql

	def _getDepartmentStatements(self):
		sql = []

		sql.append('''DROP INDEX IF EXISTS wf_username_department_username_department_index;''')
		sql.append('''ALTER TABLE wf_username_department ADD COLUMN community VARCHAR NULL;''')
		sql.append('''UPDATE wf_username_department SET community = 'default';''')
		sql.append('''ALTER TABLE wf_username_department ALTER COLUMN community SET NOT NULL;''')
		sql.append('''CREATE UNIQUE INDEX wf_username_department_community_username_department_index ON wf_username_department (community,username,department_id);''')

		return sql

	def _getSavedSetStatements(self):
		sql = []

		sql.append('''ALTER TABLE wf_uber_saved_set ADD COLUMN community VARCHAR NULL;''')
		sql.append('''UPDATE wf_uber_saved_set SET community = 'default';''')
		sql.append('''ALTER TABLE wf_uber_saved_set ALTER COLUMN community SET NOT NULL;''')
		sql.append('''CREATE INDEX wf_uber_saved_set_community_index ON wf_uber_saved_set (community);''')

		return sql

	def _getReportingStatements(self):
		sql = []

		sql.append('''ALTER TABLE wf_reporting ADD COLUMN community VARCHAR NULL;''')
		sql.append('''UPDATE wf_reporting SET community = 'default';''')
		sql.append('''ALTER TABLE wf_reporting ALTER COLUMN community SET NOT NULL;''')
		sql.append('''CREATE INDEX wf_reporting_community_index ON wf_reporting (community);''')

		return sql
