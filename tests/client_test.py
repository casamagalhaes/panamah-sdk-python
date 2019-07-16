import unittest
from panamah_sdk.client import AdminClient, StreamClient

class TestClient(unittest.TestCase):
    
    def test_admin_client(self):
        """testing admin client"""
        client = AdminClient("auth")
        response = client.post("admin/assinantes", {"s": 1})
        assert(response.status_code, 200, "Erro")

    # def test_stream_client(self):
    #     """testing stream client"""
    #     client = StreamClient("auth", "secret")
    #     response = client.post("stream/data", {"s": 1})
    #     assert(response.status_code, 200, "Erro")

if __name__ == '__main__':
    unittest.main()
