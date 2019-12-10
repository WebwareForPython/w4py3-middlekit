import sys


class ModelObject(object):


    ## Debugging ##

    def printAttrs(self, out=None):
        if out is None:
            out = sys.stdout
        out.write('self = %s\n' % repr(self))
        out.write('self  attrs = %s\n' % list(self.__dict__.keys()))
        out.write('class attrs = %s\n' % list(self.__class__.__dict__.keys()))
