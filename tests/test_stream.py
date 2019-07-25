from unittest import main, mock, TestCase
from panamah_sdk.stream import PanamahStream
from panamah_sdk.models.base import Model, StringField
from panamah_sdk.models.definitions import PanamahAcesso
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response


class TestStream(TestCase):
    def test_stream(self):
        class ChildModel(Model):
            name='PRODUTO'
            schema = {
                'id': StringField(required=True)
            }

        # should not accept non-model objects on save
        stream = PanamahStream('auth', 'secret', '123')
        try:
            stream.save(None)
        except Exception as e:
            self.assertEqual(
                str(e), 'model deve ser um modelo valido do Panamah')

        # should not accept non-model objects on delete
        stream = PanamahStream('auth', 'secret', '123')
        try:
            stream.delete(None)
        except Exception as e:
            self.assertEqual(
                str(e), 'model deve ser um modelo valido do Panamah')

        # should validate models on save
        try:
            model = ChildModel()
            stream.save(model)
        except Exception as e:
            self.assertEqual(str(e), 'ChildModel.id -> propriedade obrigatoria')

        # should validate models on delete
        try:
            model = ChildModel()
            stream.delete(model)
        except Exception as e:
            self.assertEqual(str(e), 'ChildModel.id -> propriedade obrigatoria')


if __name__ == '__main__':
    main()
