import MPSCore.utilities.dbConnectionParms as dbConnParms
import MPSCore.utilities.sqlUtilities as sqlUtilities
import psycopg2
import os

createtableSQL = '''
CREATE TABLE wf_file_repo
    (id SERIAL,
    content bytea NOT NULL
    );
ALTER TABLE wf_file_repo ADD CONSTRAINT wf_file_repo_id PRIMARY KEY (id);
'''

connectionParms = dbConnParms.DbConnectionParms('localhost', 5432, 'mpsdev', 'mps', 'mps')
db = sqlUtilities.SqlUtilities(connectionParms)

content = ""

rootPath = "/Users/erpaul/Desktop/packets"

sql = "insert into wf_file_repo (content) values (%s)"

db.executeSQLCommand("delete from wf_file_repo",())


for dirname, dirnames, filenames in os.walk(rootPath):
	for fname in filenames:
		if fname.upper().endswith("PDF"):
			f = open(dirname + '/' + fname,'rb')
			content = bytearray(f.read())
			f.close()

			args = (content,)
			try:
				db.executeSQLCommand(sql,args)
			except Exception, e:
				pass


outPath = "/Users/erpaul/Desktop/packets_out/"

qry = db.executeSQLQuery("select * from wf_file_repo",())
i = 0
for each in qry:
	try:
		i +=1
		content = each['content']
		f = open(outPath + "endisAClown%i.pdf" % (i),'wb')
		f.write(bytearray(content))
		f.flush()
		f.close()
	except Exception, e:
		pass

x = 1


