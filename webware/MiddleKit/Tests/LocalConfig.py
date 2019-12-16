# LocalConfig.py
dbName = 'SQLite'
storeArgs = {'database': r'c:\Temp\test.db' }
sqlCommand = r'c:\Python38\python.exe ExecuteScript.py "%s"'
sqlVersionCommand = r'c:\Python38\python.exe ExecuteScript.py --version'



##dbName='Firebird'
##storeArgs={'database':'c:/Temp/mktemp.fdb',
##           'user':'SYSDBA','password':'masterkey'} #,
##sqlCommand='isql -q -e ' #-e to show sql stmts
##sqlVersionCommand='isql -x -z'
##DropStatements='database'
###DropStatements='tables'
###PreSQL='CREATE DOMAIN BOOLEAN AS SMALLINT CHECK (value is null or value in (0, 1)); '
###end


#dbName = 'Firebird'
#storeArgs = {'database': '/tmp/test.fdb', 'user':'SYSDBA','password':'masterkey' }
#sqlCommand = 'isql-fb -u SYSDBA -p masterkey /tmp/test.fdb  ' 
#sqlVersionCommand = 'isql-fb -x -z '

#dbName = 'MySQL'
#storeArgs = {'host':'galera-inhouse', 'user': 'root', 'passwd': 'node'}
#sqlCommand = 'mysql -h galera-inhouse -u root -pnode'
#sqlVersionCommand = 'mysql --version'
#DropStatements='tables'

#dbName='PostgreSQL'
#storeArgs={'database':'test'} #'host':'localhost','user':'nico'}
#sqlCommand='psql test ' #pg_hba.conf trust
#sqlVersionCommand='psql -V'

dbName='MSSQL'
#server=r'localhost\sqlexpress'
server=r'(localdb)\MSSQLLocalDB'
storeArgs={'driver':'{SQL Server Native Client 11.0}',
 'server':server, 'Trusted Connection':'yes'
}
sqlCommand='sqlcmd -E -S %s -i "%%s" ' % server
sqlVersionCommand='sqlcmd -E -S %s -Q"select @@version" -h-1' % server

# end
