import MPSCore.utilities.migrationFramework as MF

class Migrator(MF.MigrationHelper):
	def __init__(self,_connection):
		self.connection = _connection

	def migrate(self):
		try:
			if not self.tableExists(self.connection,"site_community"):
				siteList = self._getSites()

				for sql in self._getCommunityStatements(siteList):
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				for sql in self._getUserStatements(siteList):
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				for sql in self._getAccessLogStatements(siteList):
					self.connection.executeSQLCommand(sql, (), doCommit=False)

				self.connection.performCommit()

			return 0,""
		except Exception,e:
			self.connection.performRollback()
			return -1,e.message

	def _getSites(self):
		sql = '''SELECT * FROM site;'''
		return self.connection.executeSQLQuery(sql)

	def _getCommunityStatements(self, _siteList):
		sql = []
		sql.append('''CREATE TABLE site_community
						(id SERIAL,
						site_id INT NOT NULL,
						code VARCHAR NOT NULL,
						descr VARCHAR NOT NULL);''')
		sql.append('''ALTER TABLE site_community ADD CONSTRAINT site_community_id PRIMARY KEY (id);''')
		sql.append('''CREATE UNIQUE INDEX site_community_code_index ON site_community (site_id, code);''')

		defaultCommunitySQL = '''INSERT INTO site_community (site_id,code,descr) VALUES (%i,'default','Default');'''
		for siteDict in _siteList:
			sql.append(defaultCommunitySQL % (siteDict.get('id', 0),))

		return sql

	def _getUserStatements(self, _siteList):
		sql = []
		sql.append('''ALTER TABLE mpsuser ADD COLUMN community_id INT NULL;''')

		updateSQL = '''UPDATE mpsuser SET community_id = (SELECT id FROM site_community WHERE site_id = %i) WHERE site_id = %i;'''
		for siteDict in _siteList:
			siteId = siteDict.get('id', 0)
			sql.append(updateSQL % (siteId, siteId))

		sql.append('''ALTER TABLE mpsuser ALTER COLUMN community_id SET NOT NULL;''')
		sql.append('''ALTER TABLE mpsuser ADD CONSTRAINT mpsuser_community_fk FOREIGN KEY (community_id) REFERENCES site_community(id) DEFERRABLE INITIALLY DEFERRED;''')
		sql.append('''DROP INDEX IF EXISTS mpsuser_site_username_index;''')
		sql.append('''CREATE UNIQUE INDEX mpsuser_site_community_username_index ON mpsuser (site_id, community_id, username);''')

		return sql

	def _getAccessLogStatements(self, _siteList):
		sql = []
		sql.append('''ALTER TABLE access_log ADD COLUMN community VARCHAR NULL;''')
		sql.append('''UPDATE access_log SET community = 'Default';''')
		return sql
