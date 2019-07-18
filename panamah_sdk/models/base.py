from datetime import datetime, date
from dateutil.parser import parse as parse_date


class Model():
    values = {}
    schema = {}

    def __getattr__(self, name):
        # print('Getting attribute %s' % name)
        if name in self.schema:
            if name in self.values:
                return self.values[name]
            else:
                return self.schema[name].default if hasattr(self.schema[name], 'default') else None
        else:
            raise NameError("%s nao e uma propriedade do modelo" % name)

    def __setattr__(self, name, value):
        if name in self.schema:
            field = self.schema[name]
            self.values[name] = field.cast(
                value) if hasattr(field, 'cast') else value
        else:
            raise NameError("%s nao e uma propriedade do modelo" % name)

    def validate(self):
        for name, field in self.schema.items():
            try:
                field.validate(self.__getattr__(name))
            except Exception as error:
                raise type(error)('%s.%s -> %s' %
                                  (self.__class__.__name__, name, str(error)))


class Field():
    def __init__(self, type='unknown', required=False, default=None):
        self.type = type
        self.required = required
        self.default = default

    def validate(self, value):
        if self.required and value is None:
            raise ValueError('propriedade obrigatoria')


class StringField(Field):
    def __init__(self, allowedValues=None, required=False, default=None):
        self.allowedValues = allowedValues
        super().__init__('string', required, default)

    def validate(self, value):
        super().validate(value)
        if (not self.allowedValues is None):
            invalid_items = [
                item for item in value if item not in self.allowedValues
            ]
            if len(invalid_items) > 0:
                raise ValueError(
                    'valor(es) "%s" nao permitido(s). Somente %s' % (
                        ', '.join(invalid_items),
                        ', '.join(self.allowedValues)
                    )
                )

    def cast(self, value):
        return str(value)


class NumberField(Field):
    def __init__(self, required=False, default=None):
        super().__init__('number', required, default)

    def cast(self, value):
        return int(value)


class BooleanField(Field):
    def __init__(self, required=False, default=None):
        super().__init__('date', required, default)

    def cast(self, value):
        return bool(value)


class DateField(Field):
    def __init__(self, required=False, default=None):
        super().__init__('boolean', required, default)

    def cast(self, value):
        if isinstance(value, str):
            return parse_date(value)
        elif isinstance(value, int):
            return datetime.utcfromtimestamp(value)
        elif isinstance(value, date):
            return value
        else:
            raise ValueError('data invalida')


class ObjectField(Field):
    def __init__(self, object_class=None, required=False, default=None):
        self.object_class = object_class
        super().__init__('object', required, default)

    def validate(self, value):
        super().validate(value)
        if type(value) is self.object_class:
            value.validate()
        else:
            raise ValueError(
                'valor deve ser um modelo valido do tipo %s' % self.object_class.__name__)


class StringListField(Field):
    def __init__(self, allowedValues=None, required=False, default=None):
        self.allowedValues = allowedValues
        super().__init__('list[string]', required, default)

    def validate(self, value):
        super().validate(value)
        if (not self.allowedValues is None):
            invalid_items = [
                item for item in value if item not in self.allowedValues
            ]
            if len(invalid_items) > 0:
                raise ValueError(
                    'valor(es) "%s" nao permitido(s). Somente %s' % (
                        ', '.join(invalid_items),
                        ', '.join(self.allowedValues)
                    )
                )


class ObjectListField(Field):
    def __init__(self, object_class=None, required=False, default=None):
        self.object_class = object_class
        super().__init__('list[object]', required, default)

    def validate(self, value):
        super().validate(value)
        invalid_indexes = [
            index for (index, item) in enumerate(value) if not type(item) is self.object_class
        ]
        if len(invalid_indexes) == 0:
            for item in value:
                item.validate()
        else:
            raise ValueError(
                'objeto(s) no(s) indice(s) %s deve(m) ser modelo(s) valido(s) do tipo %s' % (
                    ', '.join([str(index) for index in invalid_indexes]), self.object_class.__name__
                )
            )
