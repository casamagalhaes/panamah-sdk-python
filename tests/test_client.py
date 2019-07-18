import unittest
from panamah_sdk.client import AdminClient, StreamClient
from .server import start as start_test_server, stop as stop_test_server, set_next_response, clear_next_response


class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_test_server()

    @classmethod
    def tearDownClass(cls):
        stop_test_server()

    def tearDown(self):
        clear_next_response()

    def test_admin_client(self):
        """testing admin client"""
        client = AdminClient("auth")
        #get
        set_next_response(200, {'id': 1})
        response = client.get("/admin/assinantes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.content, 'utf-8'), '{"id": 1}')
        #post
        set_next_response(201, {'id': 1})
        response = client.post("/admin/assinantes", {'id': 1})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(str(response.content, 'utf-8'), '{"id": 1}')

    def test_stream_client(self):
        """testing stream client"""
        client = StreamClient("auth", "secret")
        response = client.post("/stream/data", {"s": 1})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
