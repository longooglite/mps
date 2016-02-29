import MPSCore.utilities.migrationFramework as MF

class Migrator(MF.MigrationHelper):
	def __init__(self,_connection):
		self.connection = _connection

	def migrate(self):
		try:
			if not self.tableExists(self.connection,"wf_internal_evaluator"):
				sql = '''CREATE TABLE wf_internal_evaluator
							(id SERIAL,
							first_name VARCHAR NOT NULL,
							last_name VARCHAR NOT NULL,
							email_address VARCHAR NOT NULL,
							active BOOLEAN NOT NULL
							);
							ALTER TABLE wf_internal_evaluator ADD CONSTRAINT wf_internal_evaluator_id PRIMARY KEY (id);'''
				self.connection.executeSQLCommand(sql,())
			return 0,''
		except Exception,e:
			self.connection.executeSQLCommand('rollback',())
			return -1,e.message



