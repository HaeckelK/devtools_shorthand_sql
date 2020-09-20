import random
import string


class Field():
    def f(x): return ''
    test_default_function = f
    type_hint = None

    def __init__(self, sql_column_name, field_type):
        self.original_sql_column_name = sql_column_name
        self.sql_column_name = sql_column_name
        self.variable_name = sql_column_name
        self.format_variable_name_pep8()
        self.field_type = field_type
        self._test_default = None
        return

    @property
    def function_kwarg(self):
        if isinstance(self.test_default, str):
            return '"' + self.test_default + '"'
        return self.test_default

    @property
    def function_arg(self):
        return self.variable_name + ': ' + str(self.type_hint)

    @property
    def sql_query_param(self):
        return self.variable_name

    @property
    def test_default(self):
        if self._test_default is None:
            self._test_default = self.test_default_function()
        return self._test_default

    def lowercase(self):
        self.column_name = self.original_sql_column_name.lower()
        return

    def uppercase(self):
        self.column_name = self.original_sql_column_name.upper()
        return

    def format_variable_name_pep8(self):
        text = self.variable_name
        text = text.lower()
        self.variable_name = text
        return


class IntegerField(Field):
    # TODO should be signed
    def f(x): return random.randint(0, 1024)
    test_default_function = f
    type_hint = 'int'


class RealField(Field):
    def f(x): return 3.5
    test_default_function = f
    type_hint = 'float'


class TextField(Field):
    def f(x): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    test_default_function = f
    type_hint = 'str'


# TODO implement blob test
class BlobField(Field):
    pass


# TODO I need access to arg and param for IDField, need to think of another way to exclude elsewhere
class IDField(Field):
    def f(x): return 1
    test_default_function = f
    type_hint = 'int'

    @property
    def arg(self):
        return ''

    @property
    def param(self):
        return 'None'


class BooleanIntField(Field):
    def f(x): return random.choice([0, 1])
    test_default_function = f
    type_hint = 'int'
