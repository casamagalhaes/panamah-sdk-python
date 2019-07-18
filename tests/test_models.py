import unittest
from datetime import date
from panamah_sdk.models.definitions import Model, StringField, NumberField, BooleanField, DateField, ObjectField, StringListField, ObjectListField


def validate_then_expect(self, instance, message):
    try:
        instance.validate()
    except Exception as e:
        self.assertEqual(str(e), message)
        pass


def validate_then_dont_expect(self, instance, message):
    try:
        instance.validate()
    except Exception as e:
        self.assertNotEqual(str(e), message)
        pass


class TestClient(unittest.TestCase):
    def test_model(self):
        class WrongGrandChildModel(Model):
            pass

        class GrandChildModel(Model):
            pass

        class ChildModel(Model):
            schema = {
                'a': StringField(required=True),
                'b': StringField(required=True, allowedValues=['1', '2']),
                'c': StringListField(required=True, allowedValues=['1', '2']),
                'd': NumberField(required=True),
                'e': BooleanField(required=True),
                'f': DateField(required=True),
                'g': ObjectField(required=True, object_class=GrandChildModel),
                'h': ObjectListField(required=True, object_class=GrandChildModel),
            }

        # Required
        instance = ChildModel()
        validate_then_expect(
            self, instance, 'ChildModel.a -> propriedade obrigatoria')
        instance.a = 'valor preenchido'
        validate_then_dont_expect(
            self, instance, 'ChildModel.a -> propriedade obrigatoria')
        self.assertEqual(instance.a, 'valor preenchido')

        # StringField with allowedValues
        instance.b = '3'
        validate_then_expect(
            self, instance, 'ChildModel.b -> valor(es) "3" nao permitido(s). Somente 1, 2')
        instance.b = '1'
        validate_then_dont_expect(
            self, instance, 'ChildModel.b -> valor(es) "3" nao permitido(s). Somente 1, 2')

        # StringListField
        instance.c = ['1', '2', '3']
        validate_then_expect(
            self, instance, 'ChildModel.c -> valor(es) "3" nao permitido(s). Somente 1, 2')
        instance.c = ['1', '2']
        validate_then_dont_expect(
            self, instance, 'ChildModel.c -> valor(es) "3" nao permitido(s). Somente 1, 2')

        # NumberField
        instance.d = '333'
        self.assertEqual(instance.d, 333)

        # BooleanField
        instance.e = 1
        self.assertEqual(instance.e, True)
        instance.e = 0
        self.assertEqual(instance.e, False)

        # DateField
        try:
            instance.f = .0
        except Exception as e:
            self.assertEqual(str(e), 'data invalida')
        instance.f = '2019-01-03T23:59:58'
        self.assertEqual(instance.f.year, 2019)
        self.assertEqual(instance.f.month, 1)
        self.assertEqual(instance.f.day, 3)
        self.assertEqual(instance.f.hour, 23)
        self.assertEqual(instance.f.minute, 59)
        self.assertEqual(instance.f.second, 58)
        instance.f = 1546559998
        self.assertEqual(instance.f.year, 2019)
        self.assertEqual(instance.f.month, 1)
        self.assertEqual(instance.f.day, 3)
        self.assertEqual(instance.f.hour, 23)
        self.assertEqual(instance.f.minute, 59)
        self.assertEqual(instance.f.second, 58)

        # ObjectField
        instance.g = WrongGrandChildModel()
        validate_then_expect(
            self, instance, 'ChildModel.g -> valor deve ser um modelo valido do tipo GrandChildModel')
        instance.g = GrandChildModel()
        validate_then_dont_expect(
            self, instance, 'ChildModel.g -> valor deve ser um modelo valido do tipo GrandChildModel')

        # ObjectListField
        instance.h = [WrongGrandChildModel(), GrandChildModel()]
        validate_then_expect(
            self, instance, 'ChildModel.h -> objeto(s) no(s) indice(s) 0 deve(m) ser modelo(s) valido(s) do tipo GrandChildModel')
        instance.h = [GrandChildModel()]
        validate_then_dont_expect(
            self, instance, 'ChildModel.h -> objeto(s) no(s) indice(s) 0 deve(m) ser modelo(s) valido(s) do tipo GrandChildModel')


if __name__ == '__main__':
    unittest.main()
