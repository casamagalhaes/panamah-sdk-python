import unittest
from panamah_sdk.client import AdminClient, StreamClient
from .test_server import start as start_test_server, stop as stop_test_server

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        start_test_server()

    @classmethod
    def tearDownClass(cls):
        stop_test_server()

    def test_admin_client(self):
        """testing admin client"""
        client = AdminClient("auth")
        response = client.get("/admin/assinantes")
        self.assertEqual(response.status_code, 200)

    def test_stream_client(self):
        """testing stream client"""
        client = StreamClient("auth", "secret")
        response = client.post("/stream/data", {"s": 1})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
