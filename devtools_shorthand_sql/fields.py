import random


class Field():
    test_default_function = lambda x: ''
    type_hint = None
    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type
        # TODO is this right way to do this?
        self._test_default = None
        return

    @property
    def kwarg(self):
        if isinstance(self.test_default, str):
            return '"' + self.test_default + '"'
        return self.test_default

    @property
    def arg(self):
        return self.name + ': ' + str(self.type_hint)

    @property
    def param(self):
        return self.name

    @property
    def test_default(self):
        if self._test_default is None:
            self._test_default = self.test_default_function()
        return self._test_default

    def lowercase(self):
        self.name = self.name.lower()
        return

    def uppercase(self):
        self.name = self.name.upper()
        return


class IntegerField(Field):
    test_default_function = lambda x: random.randrange(-1024, 1024)
    type_hint = 'int'


class RealField(Field):
    test_default_function = lambda x: 3.5
    type_hint = 'float'


class TextField(Field):
    test_default_function = lambda x: '123fakestreet'
    type_hint = 'str'


# TODO implement blob test
class BlobField(Field):
    pass


class IDField(Field):
    test_default_function = lambda x: 1
    type_hint = 'int'

    @property
    def arg(self):
        return ''

    @property
    def param(self):
        return 'None'


class BooleanIntField(Field):
    test_default_function = lambda x: 0
    type_hint = 'int'