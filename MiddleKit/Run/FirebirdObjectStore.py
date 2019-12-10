#@@retruning id

#connectionPool = False
from fdb import DatabaseError
import fdb as dbi
def QuotedString(s):
    return "'%s'" % s.replace("\\", "\\\\").replace("'", "''")

#from MiscUtils import NoDefault
#from MiscUtils.MixIn import MixIn
#from MiddleKit.Run.ObjectKey import ObjectKey
#from MiddleObject import MiddleObject

from .SQLObjectStore import SQLObjectStore, UnknownSerialNumberError


class FirebirdObjectStore(SQLObjectStore):
    def dbapiVersion(self):
        """Return the version of the DB API module."""
        module = self.dbapiModule()
        return '%s %s' % (module.__name__, module.__version__)

    def dbVersion(self ):
        return 'embedded'
    

    """implements an object store backed by a registered Firebird 2.x database.

    
    """

    def augmentDatabaseArgs(self, args, pool=False):
        if not args.get('database'):
            args['database'] = self._model.sqlDatabaseName()
        if not args.get('user'):
            args['user']='SYSDBA'
            args['password']='masterkey'
            
    def newConnection(self):
        args = self._dbArgs.copy()
        self.augmentDatabaseArgs(args)
        conn=self.dbapiModule().connect( **args)
        return conn

    
    
    def newCursorForConnection(self, conn, dictMode=True):
        #dictMode seems to be not used?
        return conn.cursor()

    #def retrieveNextInsertId(self, klass):
    #    #return None ##if retruning serialNum
    #    seqname = "GEN_%s_ID" % klass.name().upper()
    #    #return 'GEN_ID(%s,1)' % seqname 
    #    conn, curs = self.executeSQL("select GEN_ID(%s,1) from rdb$database" % seqname )
    #    value = curs.fetchone()[0]
    #    ##assert value, "Didn't get next id value from sequence"
    #    return value
    def retrieveLastInsertId(self, conn, cur):
        #raise Exception("unsupported lastrowid")
        #requires extended syntax patch, "returning serialNum"
        
        return cur.fetchone()[0]
    
    def dbapiModule(self):
        return dbi

    def _executeSQL(self, cur, sql, clausesArgs=None ):
        
        if '_MKClassIds' in sql:
            sql = sql.replace('_MKClassIds','"_MKClassIds"')

        if sql.startswith('insert into '):
            sql =  sql[:-1] + " returning serialNum" #%callers.klass @@.sqlSerialColumnName()

        #print sql , clausesArgs or ''
        try:
            print( "FB>", sql, clausesArgs or '')
            cur.execute( sql, clausesArgs or tuple() )
        except Warning:
            if not self.setting('IgnoreSQLWarnings', False):
                raise

    def saveChanges(self):
        conn, cur = self.connectionAndCursor()
        try:
            SQLObjectStore.saveChanges(self)
        except DatabaseError:
            conn.rollback()
            raise
        except Warning:
            if not self.setting('IgnoreSQLWarnings', False):
                conn.rollback()
                raise
        conn.commit()
    def revertChanges(self ):
        conn,cur = self.connectionAndCursor()
        conn.rollback()
        
    def sqlCaseInsensitiveLike(self, a, b):
        return "lower(%s ) like lower(%s)" % (a, b)
        #return "lower(%s ) similar to lower(%s)" % (a, b)

    def sqlNowCall(self):
        return 'CURRENT_TIME '



#from string import lower 
class Klass(object):

    def sqlTableName(self):
        x = self.name()
        
        if x.lower() in ('role',):
            return '"Role"'
        elif x=='Order':
            return 'Orders'
        else:
            return self.name()
        
        


dont_use_columnnames=('year','timestamp','date', 'value', 'e') ##sorry, is duplicated in Design
class Attr(object):
    def sqlColumnName(self ):
        Attr.mixInSuperSqlColumnName(self)
        x = self._sqlColumnName
        if x.lower() in dont_use_columnnames: #map(lower,dont_use_columnnames ) :
            self._sqlColumnName= '"%s"' % x.upper()
        return self._sqlColumnName
    
        

##class ObjRefAttr(object):
##    def sqlColumnName(self ):
##        ObjRefAttr.mixInSuperSqlColumnName(self)
##        
##        
        
class StringAttr(object):

    def sqlForNonNone(self, value):
        return "%s" % QuotedString( value)


class BoolAttr(object):

    def sqlForNonNone(self, value):
        #return int(value) #Design needs int? boolean domain
        return str(int(value))
