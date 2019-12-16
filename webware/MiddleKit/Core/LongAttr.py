from .BasicTypeAttr import BasicTypeAttr


class LongAttr(BasicTypeAttr):

    def __init__(self, attr):
        BasicTypeAttr.__init__(self, attr)
        if self.get('Max') is not None:
            self['Max'] = int(self['Max'])
        if self.get('Min') is not None:
            self['Min'] = int(self['Min'])
