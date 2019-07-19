from unittest import main, mock, TestCase
from panamah_sdk.stream import PanamahStream
from panamah_sdk.models.base import Model, StringField
from panamah_sdk.models.definitions import PanamahAcesso
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response


class TestStream(TestCase):
    def test_stream(self):
        class ChildModel(Model):
            schema = {
                'a': StringField(required=True)
            }

        # should not accept non-model objects
        stream = PanamahStream('auth', 'secret')
        try:
            stream.save(None)
        except Exception as e:
            self.assertEqual(
                str(e), 'model deve ser um modelo valido do Panamah')

        # should validate models
        try:
            model = ChildModel()
            stream.save(model)
        except Exception as e:
            self.assertEqual(str(e), 'ChildModel.a -> propriedade obrigatoria')


if __name__ == '__main__':
    main()
