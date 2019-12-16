#  [1] still problems with default 11 (according to the docs it should work? incl. gen_id(kkk_seq,1)
#@@isDerived || computed by ( formulaa ), enum -> Domains 
#@@_MKClassIds must be quted (patch necessary)
#@@beside this parametrized executions should be executed


from fdb import DatabaseError
#def QuotedString(s):
#    return "'%s'" % s.replace("\\", "\\\\").replace("'", "''")

#from MiscUtils.MixIn import MixIn

from .SQLGenerator import SQLGenerator
#from SQLGenerator import PrimaryKey as PrimaryKeyBase


class FirebirdSQLGenerator(SQLGenerator):

    def sqlSupportsDefaultValues(self):
        return True
    

class Model(object):
    def writeConnectToDatabase(self, generator, output, databasename):
        output.write("connect 'c:/Temp/mktemp.fdb' user 'SYSDBA' password 'masterkey' ;\n\n" ) #% databasename)

    


class Klasses(object):
    def writeClassIdsSQL(self, generator, out):
        wr = out.write
        #-- set autoddl on; isql default
        wr('''
 CREATE DOMAIN BOOLEAN AS SMALLINT CHECK (value is null or value in (0, 1));

create table "_MKClassIds" (
id int not null primary key,
name varchar(100)
);
''')
        #wr('delete from "_MKClassIds"; \n\n')
        for klass in self._model._allKlassesInOrder:
            wr('insert into "_MKClassIds" (id, name) values ')
            wr("    (%s, '%s');\n" % (klass.id(), klass.name()))
        wr('commit;\n') #autoddl on doenst meen commit insert stmts;-)
    

    def dropDatabaseSQL(self, dbName):
        return ''

    def dropTablesSQL(self):
        sql = []
        #for tableName in reversed(self.auxiliaryTableNames()):
        #    sql.append('drop table "%s";\n' % tableName)
        for klass in reversed(self._model._allKlassesInOrder):
            #sql.append('drop generator "%s_GEN_ID";\n' % klass.name())
            sql.append('drop table "%s";\n' % klass.name())
        sql.append('\n')
        return ''.join(sql)

    def createDatabaseSQL(self, dbName):
        return "create database 'c:/Temp/mktemp.fdb' user 'SYSDBA' password 'masterkey'; \n"
        return ''

    def useDatabaseSQL(self, dbName):
        return ''

    def listTablesSQL(self):
        #return "show tables;\n"
        #according to http://www.firebirdfaq.org/faq174/
        return "show tables; "
##        return """
##            select rdb$relation_name
##             from rdb$relations
##             where rdb$view_blr is null 
##             and (rdb$system_flag is null or rdb$system_flag = 0);
##        """

#from string import lower 
dont_use_relnames=('Role',)  
class Klass(object):
    def writeCreateSQL(self, generator, out):
        # create the sequences explicitly, just to be sure
        wr = out.write
        if not self.isAbstract():
            wr('create generator %s ;\n\n' % self.seqName())
        Klass.mixInSuperWriteCreateSQL(self, generator, out)
        #self.writePgSQLIndexDefs(wr)

    def seqName(self):
        return 'GEN_%s_id' % (self.name() , )
    def sqlTableName(self):
        """Return table name.

        Returns quoted table name if necessary

        """
        tn = self.name()
        if tn[0]=='_' or tn.lower() in list(dont_use_relnames) :
            return '"%s"' % tn
        else:
            return tn
    def writePostCreateTable(self, generator, out):
        wr = out.write
        #@@write all defaults now
        # alter table TABLE  alter COLUMN set default  DEFAULT  ;
        if not self.isAbstract():
            sn = self.sqlSerialColumnName() 
            wr("""set term !! ;
CREATE TRIGGER %s_BI FOR %s
ACTIVE BEFORE INSERT POSITION 0
AS
BEGIN
  IF (NEW.%s IS NULL) THEN
    NEW.%s = GEN_ID(%s, 1);
END!!
set term ; !!


""" % ( self.seqName(), self.name(), sn, sn, self.seqName() )  )
            
dont_use_columnnames=('value','year','e') 
class Attr(object):
    def sqlName(self):
        x= self.name()
        if x.lower() in list(dont_use_columnnames ):
            return '"%s"' % x.upper()
        else:
            return x
    
    
    #def sqlColumnName(self):
    #   """Return the SQL column name corresponding to this attribute."""
        
class StringAttr(object):

    def sqlType(self):
        # @@ 2000-11-11 ce: cache this
        if not self.get('Max'):
            return 'varchar(100) /* WARNING: NO LENGTH SPECIFIED */'
        max = int(self['Max']) # @@ 2000-11-12 ce: won't need int() after using types
        if max > 32765 :
            return 'blob sub_type text '
        if self.get('Min') and int(self['Min']) == max:
            return 'char(%s)' % max
        else:
            return 'varchar(%s)' % max

    def sqlForNonNoneSampleInput(self, value):
        #return "%s" % QuotedString(value)
        return "'%s'" % value.replace("'", "''")
    

class BoolAttr(object):
    def sqlType(self ):
        return 'boolean'
        #needs """CREATE DOMAIN BOOLEAN AS SMALLINT CHECK (value is null or value in (0, 1));"""
        #http://www.firebirdfaq.org/faq12/


        #return 'char(1)'
    def _u_sqlForNonNoneSampleInput(self, value):
        return value in ( '1','true','on', 1 )
    
        #assert int(value) in (0,1), Exception(
        #    "'%s' is not a valid default for boolean column '%s'"
        #    % (value, self.name()))
        #return value

class FloatAttr(object):

    def sqlType(self):
        return 'float'
        # return 'decimal(16,8)'
        # ^ use the decimal type instead

    def sampleValue(self, value):
        float(value) # raises exception if value is invalid
        return value

class MoneyAttr(object):
    def sqlType(self):
        return 'decimal(18,4)'
    
#class EnumAttr(object):


    
class DateAttr(object):
    def sqlType(self ):
        return 'date'
class DateTimeAttr(object):

    def sqlType(self):
        return 'timestamp'


class ObjRefAttr(object):
    def classIdReferences(self):
        return ' references "_MKClassIds"'
    def sqlType(self):
        if self.setting('UseBigIntObjRefColumns', False):
            return 'bigint '
        else:
            return 'integer /* %s */' % self['Type']
        
class ListAttr(object):

    def sqlType(self):
        #raise TypeError('Lists do not have a SQL type.')
        return 'array'

