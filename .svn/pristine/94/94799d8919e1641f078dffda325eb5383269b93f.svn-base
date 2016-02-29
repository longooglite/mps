import os.path
import sys
sys.path.append(os.path.abspath(__file__).split("car")[0] + "car" + os.sep)
import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.sqlUtilities as sqlUtils
from psycopg2.extensions import lobject


class Lobber():

	def run(self):
		conn = self.getConnection()
		conn.executeSQLCommand('DROP TABLE IF EXISTS test')
		conn.executeSQLCommand('CREATE TABLE test (id SERIAL,file_name VARCHAR,oid INT)')
		conn.executeSQLCommand('ALTER TABLE test ADD CONSTRAINT test_pk PRIMARY KEY (id)')

		conn.executeSQLCommand('''INSERT INTO test (file_name,oid) VALUES ('clinton.pdf', lo_import('/tmp/pdf/file_2fd551c9fb2c4385b52e63eefa764167.pdf'))''')
		rows = 	conn.executeSQLQuery('''SELECT * FROM test''')
		row1 = rows[0]
		import pprint;pprint.pprint(row1)

		goop = conn.executeSQLQuery('''SELECT pageno,data from pg_largeobject where loid=%s ORDER BY pageno''', (row1.get('oid',0),))
		import pprint;pprint.pprint(goop)

#		it = lobject(conn.getMpsConnection(), row1.get('oid',0), 'r')
#		data = it.read()
#		ignoredOut = conn.executeSQLQuery("SELECT lo_export(test.oid, '/tmp/pdf/clinton.pdf') FROM test WHERE file_name='clinton.pdf'")
		out = open('/tmp/pdf/clinton.pdf','w')
		for aDict in goop:
			out.write(aDict.get('data','')[0:])
		out.close()
		pass

	def getConnection(self):
		parms = dbConnParms.DbConnectionParms(host='localhost', port=5432, dbname='mpsdev', username='mps', password='mps')
		return sqlUtils.SqlUtilities(parms)

Lobber().run()
