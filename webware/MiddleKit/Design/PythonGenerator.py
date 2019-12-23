
import os
import sys
import datetime

from .CodeGenerator import CodeGenerator
from webware.MiscUtils import AbstractError
from MiddleKit.Core.ObjRefAttr import objRefJoin


class PythonGenerator(CodeGenerator):

    def generate(self, dirname):
        self.requireDir(dirname)
        # @@ 2000-10-17 ce: ACK! Get rid of all these hard coded 'GeneratedPy' strings
        # @@ 2000-10-16 ce: should delete GeneratedPy/
        self.requireDir(os.path.join(dirname, 'GeneratedPy'))
        self.writeInfoFile(os.path.join(dirname, 'GeneratedPy', 'Info.text'))
        self._model.writePy(self, dirname)


class Model(object):

    def writePy(self, generator, dirname):
        self._klasses.assignClassIds(generator)

        if self.hasSetting('Package'):
            filename = os.path.join(dirname, '__init__.py')
            if not os.path.exists(filename):
                open(filename, 'w').write('#')

        for klass in self._allKlassesInOrder:
            filename = os.path.join(dirname, klass.name() + '.py')
            klass.writePyStubIfNeeded(generator, filename)

            filename = os.path.join(dirname, 'GeneratedPy', 'Gen' + klass.name() + '.py')
            klass.writePy(generator, filename)

        filename = os.path.join(dirname, 'GeneratedPy', '__init__.py')
        open(filename, 'w').write('# __init__.py\n')


class ModelObject(object):

    def writePy(self, generator, out=sys.stdout):
        """Write the Python code to define a table for the class.

        The target can be a file or a filename.
        """
        if isinstance(out, str):
            out = open(out, 'w')
            close = True
        else:
            close = False
        self._writePy(generator, out)
        if close:
            out.close()


class Klass(object):

    def writePyStubIfNeeded(self, generator, filename):
        if not os.path.exists(filename):
            # Grab values for use in writing file
            basename = os.path.basename(filename)
            name = self.name()
            superclassModule = 'GeneratedPy.Gen' + name
            superclassName = 'Gen' + name

            # Write file
            with open(filename, 'w') as f:
                f.write(PyStubTemplate % locals())

    def _writePy(self, generator, out):
        self._pyGenerator = generator
        self._pyOut = out
        self.writePyFileDocString()
        self.writePyAttrCaches()
        self.writePyImports()
        self.writePyClassDef()

    def writePyFileDocString(self):
        wr = self._pyOut.write
        out = self._pyOut
        wr("""'''\n""")
        wr('Gen%s.py\n' % self.name())
        # wr('%s\n' % asctime(localtime()))
        wr('Generated by MiddleKit.\n')  # @@ 2000-10-01 ce: Put the version number here
        wr("""'''\n""")

    def writePyAttrCaches(self):

        wr = self._pyOut.write
        wr('''
# MK attribute caches for setFoo() methods
''')
        for attr in self.allAttrs():
            wr('_%sAttr = None\n' % attr.name())
        wr('\n')

    def writePyImports(self):
        wr = self._pyOut.write
        wr('''
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from webware.MiscUtils.DateParser import parseDateTime, parseDate, parseTime
from MiddleKit.Run.MiddleObject import MiddleObject
''')
        supername = self.supername()
        if supername == 'MiddleObject':
            wr('\n\nfrom MiddleKit.Run.MiddleObject import MiddleObject\n')
        else:
            pkg = self._klasses._model.setting('Package', '')
            if pkg:
                pkg += '.'
            # backPath = repr('../' * (pkg.count('.') + 1))
            backPath = 'dirname(__file__)'
            for i in range(pkg.count('.') + 1):
                backPath = 'dirname(%s)' % backPath
            wr('''\
import sys
from os.path import dirname
sys.path.insert(0, %(backPath)s)
from %(pkg)s%(supername)s import %(supername)s
del sys.path[0]

''' % locals())

    def writePyClassDef(self):
        wr = self._pyOut.write
        wr('\n\nclass Gen%s(%s):\n' % (self.name(), self.supername()))
        self.writePyInit()
        self.writePyReadStoreData()
        self.writePyAccessors()
        wr('\n')

    def maxAttrNameLen(self):
        return max([len(attr.name()) for attr in self.attrs()] or [0])

    def writePyInit(self):
        wr = self._pyOut.write
        wr('\n    def __init__(self):\n')
        wr('        %s.__init__(self)\n' % self.supername())
        maxLen = self.maxAttrNameLen()
        for attr in self.attrs():
            name = attr.name().ljust(maxLen)
            wr('        self._%s = %r\n' % (name, attr.defaultValue()))
        wr('\n')

    def writePyReadStoreData(self):
        wr = self._pyOut.write
        statements = [attr.pyReadStoreDataStatement() for attr in self.attrs()]
        statements = [s for s in statements if s]
        if statements:
            wr('''
    def readStoreData(self, store, row):
        if not self._mk_inStore:
''')
            for s in statements:
                wr(s)
            wr('        %s.readStoreData(self, store, row)\n\n' % self.supername())

    def writePyAccessors(self):
        """Write Python accessors for attributes simply by asking each one to do so."""
        out = self._pyOut
        for attr in self.attrs():
            attr.writePyAccessors(out)


class Attr(object):

    def defaultValue(self):
        """Return the default value as a legal Pythonic value."""
        if 'Default' in self:
            default = self['Default']
            if isinstance(default, str):
                default = default.strip()
            if not default:
                return None
            else:
                return self.stringToValue(default)
        else:
            return None

    def stringToValue(self, string):
        # @@ 2000-11-25 ce: consider moving this to Core
        # @@ 2000-11-25 ce: also, this might be usable in the store
        """Return a bona fide Python value given a string.

        Invokers should never pass None or blank strings.
        Used by at least defaultValue(). Subclass responsibility.
        """
        raise AbstractError(self.__class__)

    def pyReadStoreDataStatement(self):
        return None

    def writePyAccessors(self, out):
        self.writePyGet(out)
        self.writePySet(out)
        if self.setting('AccessorStyle', 'methods') == 'properties':
            out.write('\n\n    %s = property(%s, %s)\n\n' % (
                self.name(), self.pyGetName(), self.pySetName()))

    def writePyGet(self, out):
        out.write('''
    def %s(self):
        return self._%s
''' % (self.pyGetName(), self.name()))

    def writePySet(self, out):
        name = self.name()
        pySetName = self.pySetName()
        out.write('\n    def %(pySetName)s(self, value):\n' % locals())
        self.writePySetChecks(out)
        self.writePySetAssignment(out.write, name)

    def writePySetAssignment(self, write, name):
        write('''
        # set the attribute
        origValue = self._%(name)s
        self._%(name)s = value

        # MiddleKit machinery
        if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
            global _%(name)sAttr
            if _%(name)sAttr is None:
                _%(name)sAttr = self.klass().lookupAttr('%(name)s')
                if not _%(name)sAttr.shouldRegisterChanges():
                    _%(name)sAttr = 0
            if _%(name)sAttr:
                # Record that it has been changed
                self._mk_changed = True
                if self._mk_changedAttrs is None:
                    self._mk_changedAttrs = {}  # maps name to attribute
                self._mk_changedAttrs['%(name)s'] = _%(name)sAttr  # changedAttrs is a set
                # Tell ObjectStore it happened
                self._mk_store.objectChanged(self)
''' % {'name': name})

    def writePySetChecks(self, out):
        if self.isRequired():
            out.write('        assert value is not None\n')


PyStubTemplate = """\
'''
%(basename)s
'''

if not __package__:
    __package__='MiddleKit.Tests.WorkDir'
from .%(superclassModule)s import %(superclassName)s


class %(name)s(%(superclassName)s):

    def __init__(self):
        %(superclassName)s.__init__(self)
"""


class BoolAttr(object):

    def stringToValue(self, string):
        try:
            string = string.upper()
        except Exception:
            pass
        if string in (True, 'TRUE', 'YES', '1', '1.0', 1, 1.0):
            value = True
        elif string in (False, 'FALSE', 'NO', '0', '0.0', 0, 0.0):
            value = False
        else:
            value = int(string)
            assert value in (0, 1), value
            value = bool(value)
        return value

    def writePySetChecks(self, out):
        #Attr.writePySetChecks.__func__(self, out)
        Attr.writePySetChecks(self, out)
        out.write('''\
        if value is not None:
            if not isinstance(value, (bool, int)):
                raise TypeError('expecting bool or int for bool, but got value %r of type %r instead' % (value, type(value)))
            if value not in (True, False, 1, 0):
                raise ValueError('expecting True, False, 1 or 0 for bool, but got %s instead' % value)
''')


class IntAttr(object):

    def stringToValue(self, string):
        return int(string)

    def writePySetChecks(self, out):
        #Attr.writePySetChecks.__func__(self, out)
        Attr.writePySetChecks(self, out)
        out.write('''\
        if value is not None:
            if isinstance(value, int):
                value = int(value)
                #if isinstance(value, int):
                #    raise OverflowError(value)
            elif not isinstance(value, int):
                raise TypeError('expecting int type, but got value %r of type %r instead' % (value, type(value)))
''')


class LongAttr(object):

    def stringToValue(self, string):
        return int(string)

    def writePySetChecks(self, out):
        #Attr.writePySetChecks.__func__(self, out)
        Attr.writePySetChecks(self, out)
        out.write('''\
        if value is not None:
            if isinstance(value, int):
                value = int(value)
            elif not isinstance(value, int):
                raise TypeError('expecting int type, but got value %r of type %r instead' % (value, type(value)))
''')


class FloatAttr(object):

    def stringToValue(self, string):
        return float(string)

    def writePySetChecks(self, out):
        #Attr.writePySetChecks.__func__(self, out)
        Attr.writePySetChecks(self, out)
        out.write('''\
        if value is not None:
            if isinstance(value, int):
                value = float(value)
            elif not isinstance(value, float):
                raise TypeError('expecting float type, but got value %r of type %r instead' % (value, type(value)))
''')


class DecimalAttr(object):

    def stringToValue(self, string):
        return float(string)

    def writePySetChecks(self, out):
        #Attr.writePySetChecks.__func__(self, out)
        Attr.writePySetChecks(self, out)
        out.write('''\
        if value is not None:
            if isinstance(value, int):
                value = float(value)
            elif isinstance(value, float):
                value = Decimal(str(value))
            elif not isinstance(value, Decimal):
                raise TypeError('expecting decimal type, but got value %r of type %r instead' % (value, type(value)))
''')


class StringAttr(object):

    def stringToValue(self, string):
        return string

    def writePySetChecks(self, out):
        #Attr.writePySetChecks.__func__(self, out)
        Attr.writePySetChecks(self, out)
        out.write('''\
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('expecting string type, but got value %r of type %r instead' % (value, type(value)))
''')


class EnumAttr(object):

    def stringToValue(self, string):
        if self.usesExternalSQLEnums():
            return self.intValueForString(string)
        else:
            return string

    def writePyAccessors(self, out):
        #Attr.writePyAccessors.__func__(self, out)
        Attr.writePyAccessors(self, out)
        if self.setting('ExternalEnumsSQLNames')['Enable']:
            name = self.name()
            getName = self.pyGetName()
            out.write('''
    def %(getName)sString(self):
        global _%(name)sAttr
        if _%(name)sAttr is None:
            _%(name)sAttr = self.klass().lookupAttr('%(name)s')
        return _%(name)sAttr.enums()[self._%(name)s]
''' % locals())
            if self.setting('AccessorStyle', 'methods') == 'properties':
                out.write('\n\n    %(name)sString = property(%(getName)sString,'
                    ' "Returns the string form of %(name)s'
                    ' (instead of the integer value).")\n\n' % locals())

    def writePySetChecks(self, out):
        #Attr.writePySetChecks.__func__(self, out)
        Attr.writePySetChecks(self, out)
        out.write('''\
        global _%(name)sAttr
        if _%(name)sAttr is None:
            _%(name)sAttr = self.klass().lookupAttr('%(name)s')
''' % {'name': self.name()})
        if self.usesExternalSQLEnums():
            out.write('''
        if value is not None:
            if isinstance(value, str):
                try:
                    value = _%(name)sAttr.intValueForString(value)
                except KeyError:
                    raise ValueError('expecting one of %%r, but got %%r instead' %% (_%(name)sAttr.enums(), value))
            elif not isinstance(value, int):
                raise TypeError('expecting int type for enum, but got value %%r of type %%r instead' %% (value, type(value)))
            if not _%(name)sAttr.hasEnum(value):
                raise ValueError('expecting one of %%r, but got %%r instead' %% (_%(name)sAttr.enums(), value))
''' % {'name': self.name()})
        else:
            out.write('''
        if value is not None:
            if not isinstance(value, str):
                raise TypeError('expecting string type for enum, but got value %%r of type %%r instead' %% (value, type(value)))
            attr = self.klass().lookupAttr('%s')
            if not attr.hasEnum(value):
                raise ValueError('expecting one of %%r, but got %%r instead' %% (attr.enums(), value))
''' % self.name())
            # @@ 2001-07-11 ce: could optimize above code

    def writePySetAssignment(self, write, name):
        write('''
        # set the attribute
        origValue = self._%(name)s
        self._%(name)s = value

        # MiddleKit machinery
        if not self._mk_initing and self._mk_serialNum>0 and value is not origValue:
            # Record that it has been changed
            self._mk_changed = 1
            if self._mk_changedAttrs is None:
                self._mk_changedAttrs = {}  # maps name to attribute
            self._mk_changedAttrs['%(name)s'] = _%(name)sAttr  # changedAttrs is a set
            # Tell ObjectStore it happened
            self._mk_store.objectChanged(self)
''' % {'name': name})


    ## Settings ##

    def usesExternalSQLEnums(self):
        # @@ 2004-02-25 ce: seems like this method and its use
        # should be pushed down to SQLPythonGenerator.py
        flag = getattr(self, '_usesExternalSQLEnums', None)
        if flag is None:
            flag = self.model().usesExternalSQLEnums()
            self._usesExternalSQLEnums = flag
        return flag


class AnyDateTimeAttr(object):

    def writePySetChecks(self, out):
        #Attr.writePySetChecks.__func__(self, out)
        Attr.writePySetChecks(self, out)
        typeName = self.nativeDateTimeTypeName()
        if not isinstance(typeName, str):
            typeName = '(%s)' % ', '.join(typeName)
        out.write('''\
        if value is not None:
            if isinstance(value, str):
                value = %s(value)
            if not isinstance(value, %s):
                raise TypeError('expecting %s type (e.g., %s), but got'
                    ' value %%r of type %%r instead' %% (value, type(value)))
''' % (self.nativeDateTimeParser(), typeName, self['Type'], typeName))

    def writePyGet(self, out):
        out.write('''
    def %s(self):
        return self._%s
''' % (self.pyGetName(), self.name()))


class DateAttr(object):

    def nativeDateTimeTypeName(self):
        return 'date'

    def nativeDateTimeParser(self):
        return 'parseDate'

    def writePySetChecks(self, out):
        # additional check to also allow datetime instances
        out.write('''\
        if isinstance(value, datetime):
            value = value.date()
''')
        DateAttr.mixInSuperWritePySetChecks(self, out)
        #Attr.writePySetChecks(self, out)


class TimeAttr(object):

    def nativeDateTimeTypeName(self):
        return ('time', 'timedelta')

    def nativeDateTimeParser(self):
        return 'parseTime'

    def writePySetChecks(self, out):
        # additional check to also allow datetime instances
        out.write('''\
        if isinstance(value, datetime):
            value = value.time()
''')
        TimeAttr.mixInSuperWritePySetChecks(self, out)
        #Attr.writePySetChecks(self, out)


class DateTimeAttr(object):

    def nativeDateTimeTypeName(self):
        return 'datetime'

    def nativeDateTimeParser(self):
        return 'parseDateTime'


class ObjRefAttr(object):

    def stringToValue(self, string):
        parts = string.split('.', 2)
        if len(parts) == 2:
            className, objSerialNum = parts
        else:
            className = self.targetClassName()
            objSerialNum = string
        klass = self.klass().klasses()._model.klass(className)
        klassId = klass.id()
        objRef = objRefJoin(klassId, int(objSerialNum))
        return objRef

    def writePySet(self, out):
        name = self.name()
        pySetName = self.pySetName()
        targetClassName = self.targetClassName()
        package = self.setting('Package', '')
        if package:
            package += '.'
        if self.isRequired():
            reqAssert = 'assert value is not None'
        else:
            reqAssert = ''
        out.write('''
    def %(pySetName)s(self, value):
        %(reqAssert)s
        if value is not None and not isinstance(value, int):
            if not isinstance(value, MiddleObject):
                raise TypeError('expecting a MiddleObject, but got value %%r of type %%r instead' %% (value, type(value)))
            from %(package)s%(targetClassName)s import %(targetClassName)s
            if not isinstance(value, %(targetClassName)s):
                raise TypeError('expecting %(targetClassName)s, but got value %%r of type %%r instead' %% (value, type(value)))
''' % locals())
        self.writePySetAssignment(out.write, name)


class ListAttr(object):

    def defaultValue(self):
        """Return the default value as a legal Pythonic value."""
        assert not self.get('Default', 0), 'Cannot have default values for lists.'
        return []

    def pyReadStoreDataStatement(self):
        # Set the lists to None on the very first read from the store
        # so the list get methods will fetch the lists from the store.
        return '            self._%s = None\n' % self.name()

    def writePyAccessors(self, out):
        # Create various name values that are needed in code generation
        name = self.name()
        pyGetName = self.pyGetName()
        pySetName = self.pySetName()
        capName = name[0].upper() + name[1:]
        sourceClassName = self.klass().name()
        targetClassName = self.className()
        backRefAttrName = self.backRefAttrName()
        upperBackRefAttrName = backRefAttrName[0].upper() + backRefAttrName[1:]
        package = self.setting('Package', '')
        if package:
            package += '.'
        names = locals()

        # Invoke various code gen methods with the names
        self.writePyGet(out, names)
        self.writePyAddTo(out, names)
        self.writePyDelFrom(out, names)

    def writePyGet(self, out, names):
        """Subclass responsibility."""
        raise AbstractError(self.__class__)

    def writePySet(self, out, names=None):
        """Write code for setter.

        Raise an exception in order to ensure that our inherited "PySet"
        code generation is used.
        """
        raise AssertionError('Lists do not have a set method.')

    def writePyAddTo(self, out, names):
        names['getParens'] = '()' if self.setting(
            'AccessorStyle', 'methods') == 'methods' else ''
        out.write('''
    def addTo%(capName)s(self, value):
        assert value is not None
        from %(package)s%(targetClassName)s import %(targetClassName)s
        assert isinstance(value, %(targetClassName)s)
        assert value.%(backRefAttrName)s%(getParens)s is None
        self.%(pyGetName)s().append(value)
        value.setValueForKey('%(backRefAttrName)s', self)
        store = self.store()
        if value.serialNum() == 0 and self.isInStore():
            store.addObject(value)
''' % names)
        del names['getParens']

    def writePyDelFrom(self, out, names):
        names['getParens'] = '()' if self.setting(
            'AccessorStyle', 'methods') == 'methods' else ''
        out.write('''
    def delFrom%(capName)s(self, value):
        assert value is not None
        from %(package)s%(targetClassName)s import %(targetClassName)s
        assert isinstance(value, %(targetClassName)s)
        assert value.%(backRefAttrName)s%(getParens)s is self
        assert value in self.%(pyGetName)s()
        self.%(pyGetName)s().remove(value)
        value.setValueForKey('%(backRefAttrName)s', None)
        store = self.store()
        if self.isInStore() and value.isInStore():
            store.deleteObject(value)
''' % names)
        del names['getParens']
