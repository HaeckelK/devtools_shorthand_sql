

class Field():
    test_default = ''
    def __init__(self, name, field_type):
        self.name = name
        self.field_type = field_type
        return

    @property
    def kwarg(self):
        if isinstance(self.test_default, str):
            return '"' + self.test_default + '"'
        return self.test_default

    def lowercase(self):
        self.name = self.name.lower()
        return

    def uppercase(self):
        self.name = self.name.upper()
        return


class IntegerField(Field):
    test_default = 999


class RealField(Field):
    test_default = 3.5


class TextField(Field):
    test_default = '123fakestreet'


# TODO implement blob test
class BlobField(Field):
    pass


class IDField(Field):
    test_default = 1