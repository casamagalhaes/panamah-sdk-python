from unittest import main, mock, TestCase
from panamah_sdk.stream import PanamahStream
from panamah_sdk.models.base import Model, StringField
from panamah_sdk.models.definitions import PanamahAcesso
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response


class TestStream(TestCase):
    def test_processor(self):
        pass        

if __name__ == '__main__':
    main()
