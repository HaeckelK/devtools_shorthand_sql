import random
import string
from typing import Optional, Any


class Field():
    type_hint = ''

    def __init__(self, sql_column_name: str, field_type: str) -> None:
        self.original_sql_column_name = sql_column_name
        self.sql_column_name = sql_column_name
        self.variable_name = sql_column_name
        self.format_variable_name_pep8()
        self.field_type = field_type
        self._test_default: Optional[str] = None
        return

    def test_default_function(self) -> Any:
        return ''

    @property
    def function_kwarg(self) -> str:
        if isinstance(self.test_default, str):
            return '"' + self.test_default + '"'
        return self.test_default

    @property
    def function_arg(self) -> str:
        return self.variable_name + ': ' + str(self.type_hint)

    @property
    def sql_query_param(self) -> str:
        return self.variable_name

    @property
    def test_default(self) -> str:
        if self._test_default is None:
            self._test_default = self.test_default_function()
        return self._test_default

    def lowercase(self) -> None:
        self.column_name = self.original_sql_column_name.lower()
        return

    def uppercase(self) -> None:
        self.column_name = self.original_sql_column_name.upper()
        return

    def format_variable_name_pep8(self) -> None:
        text = self.variable_name
        text = text.lower()
        self.variable_name = text
        return


class IntegerField(Field):
    # TODO should be signed
    type_hint = 'int'

    def test_default_function(self) -> int:
        return random.randint(0, 1024)


class RealField(Field):
    type_hint = 'float'

    def test_default_function(self) -> float:
        return 3.5


class TextField(Field):
    type_hint = 'str'

    def test_default_function(self) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


# TODO implement blob test
class BlobField(Field):
    pass


# TODO I need access to arg and param for IDField, need to think of another way to exclude elsewhere
class IDField(Field):
    type_hint = 'int'

    @property
    def arg(self) -> str:
        return ''

    @property
    def param(self) -> str:
        return 'None'

    def test_default_function(self) -> int:
        return 1


class BooleanIntField(Field):
    type_hint = 'int'

    def test_default_function(self) -> int:
        return random.choice([0, 1])
