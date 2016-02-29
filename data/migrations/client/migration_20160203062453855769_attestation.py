import MPSCore.utilities.migrationFramework as MF

class Migrator(MF.MigrationHelper):
	def __init__(self,_connection):
		self.connection = _connection

	def migrate(self):
		try:
			#place migration code here
			if (self.tableExists(self.connection, 'wf_attest')):
				if not self.columnExists(self.connection,'wf_attest','attestor_name'):
					sql = '''ALTER TABLE wf_attest ADD COLUMN attestor_name VARCHAR'''
					self.connection.executeSQLCommand(sql,())
					sql = "UPDATE wf_attest set attestor_name = '' "
					self.connection.executeSQLCommand(sql,())
					sql = "ALTER TABLE wf_attest ALTER COLUMN attestor_name SET NOT NULL;"
					self.connection.executeSQLCommand(sql,())
				if not self.columnExists(self.connection,'wf_attest','attestor_department'):
					sql = '''ALTER TABLE wf_attest ADD COLUMN attestor_department VARCHAR'''
					self.connection.executeSQLCommand(sql,())
					sql = "UPDATE wf_attest set attestor_department = '' "
					self.connection.executeSQLCommand(sql,())
					sql = "ALTER TABLE wf_attest ALTER COLUMN attestor_department SET NOT NULL;"
					self.connection.executeSQLCommand(sql,())
			return 0,""
		except Exception,e:
			self.connection.executeSQLCommand('ROLLBACK',())
			return -1,e.message

