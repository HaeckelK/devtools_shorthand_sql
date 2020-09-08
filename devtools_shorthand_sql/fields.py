

class Field():
    test_default = ''
    type_hint = None
    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type
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

    def lowercase(self):
        self.name = self.name.lower()
        return

    def uppercase(self):
        self.name = self.name.upper()
        return


class IntegerField(Field):
    test_default = 999
    type_hint = 'int'


class RealField(Field):
    test_default = 3.5
    type_hint = 'float'


class TextField(Field):
    test_default = '123fakestreet'
    type_hint = 'str'


# TODO implement blob test
class BlobField(Field):
    pass


class IDField(Field):
    test_default = 1
    type_hint = 'int'

    @property
    def arg(self):
        return ''

    @property
    def param(self):
        return 'None'