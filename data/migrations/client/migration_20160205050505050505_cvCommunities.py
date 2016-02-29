import MPSCore.utilities.migrationFramework as MF

class Migrator(MF.MigrationHelper):
	def __init__(self,_connection):
		self.connection = _connection

	def migrate(self):
		try:
			if (self.tableExists(self.connection, 'cv_person')) and \
				(not self.columnExists(self.connection, 'cv_person', 'community')):

				for sql in self._getPersonStatements():
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				for sql in self._getProxyStatements():
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				self.connection.performCommit()

			return 0,""

		except Exception,e:
			self.connection.performRollback()
			return -1,e.message

	def _getPersonStatements(self):
		sql = []

		sql.append('''DROP INDEX IF EXISTS cv_person_user_id_index;''')
		sql.append('''ALTER TABLE cv_person ADD COLUMN community VARCHAR NULL;''')
		sql.append('''UPDATE cv_person SET community = 'default';''')
		sql.append('''ALTER TABLE cv_person ALTER COLUMN community SET NOT NULL;''')
		sql.append('''CREATE UNIQUE INDEX cv_person_community_user_id_index ON cv_person (community, user_id);''')

		return sql

	def _getProxyStatements(self):
		sql = []

		sql.append('''DROP INDEX IF EXISTS cv_proxy_grantor_index;''')
		sql.append('''DROP INDEX IF EXISTS cv_proxy_grantee_index;''')
		sql.append('''ALTER TABLE cv_proxy ADD COLUMN grantor_community VARCHAR NULL;''')
		sql.append('''ALTER TABLE cv_proxy ADD COLUMN grantee_community VARCHAR NULL;''')
		sql.append('''UPDATE cv_proxy SET grantor_community = 'default';''')
		sql.append('''UPDATE cv_proxy SET grantee_community = 'default';''')
		sql.append('''ALTER TABLE cv_proxy ALTER COLUMN grantor_community SET NOT NULL;''')
		sql.append('''ALTER TABLE cv_proxy ALTER COLUMN grantee_community SET NOT NULL;''')
		sql.append('''CREATE INDEX cv_proxy_community_grantor_index ON cv_proxy (grantor_community, grantor);''')
		sql.append('''CREATE INDEX cv_proxy_community_grantee_index ON cv_proxy (grantee_community, grantee);''')

		return sql
