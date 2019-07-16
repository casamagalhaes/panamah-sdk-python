import requests
import time
import base64
import hashlib
from .exceptions import *

GLOBAL_BASE_URL = "http://127.0.0.1:2020"  # "https://panamah.io/api/v2"
GLOBAL_SDK_IDENTITY = "panamah-python1.0.0"


class Client():
    """Base HTTP client for admin and stream"""

    def _make_request(self, method, url, payload, headers):
        response = requests.request(
            method=method, url="%s/%s" % (GLOBAL_BASE_URL, url), json=payload, headers=headers
        )
        return response

    def post(self, url, payload, headers={}):
        return self._make_request(
            "POST",
            url,
            payload,
            headers
        )

    def put(self, url, payload, headers={}):
        return self._make_request(
            "PUT",
            url,
            payload,
            headers
        )

    def delete(self, url, payload, headers={}):
        return self._make_request(
            "DELETE",
            url,
            payload,
            headers
        )

    def get(self, url, headers={}):
        return self._make_request(
            "GET",
            url,
            None,
            headers
        )


class AdminClient(Client):

    def __init__(self, authorization_token=None):
        self.authorization_token = authorization_token

    def _make_request(self, method, url, payload, headers):
        return super()._make_request(
            method,
            url,
            payload,
            {
                **headers,
                **{"Authorization": self.authorization_token}
            }
        )


class StreamClient(Client):

    def __init__(self, authorization_token=None, secret=None, assinante_id='*'):
        self.authorization_token = authorization_token
        self.secret = secret
        self.assinante_id = assinante_id
        self._tokens = None

    def _authenticate(self):
        timestamp = int(time.time())
        payload = {
            "assinanteId": self.assinante_id,
            "key": self._calculate_key(
                self.secret,
                self.assinante_id,
                timestamp
            ),
            "ts": timestamp
        }
        response = super()._make_request(
            method='POST',
            url='/stream/auth',
            payload=payload,
            headers={
                "Authorization": self.authorization_token
            }
        )
        if response.status_code == 200:
            return response.json() if response.content else None
        elif response.status_code == 403:
            raise AuthException("Credenciais invalidas")
        else:
            raise AuthException("Erro nao esperado: %d" % response.status_code)

    def _refresh_tokens(self):
        response = super()._make_request(
            method='GET',
            url='/stream/auth/refresh',
            payload=None,
            headers={
                "Authorization": self._tokens['refreshToken']
            }
        )
        if response.status_code == 200:
            return response.json() if response.content else None
        else:
            raise RefreshException(
                "Erro no refresh do token: %d" % response.status_code)

    def _calculate_key(self, secret, assinante_id, timestamp):
        return base64.b64encode(hashlib.sha1((secret + assinante_id + str(timestamp)).encode('utf-8')).digest()).decode('utf-8')

    def _make_authenticated_request(self, method, url, payload, headers):
        response = super()._make_request(
            method,
            url,
            payload,
            {
                **headers,
                **{
                    "Authorization": self._tokens["accessToken"]
                }
            }
        )
        if response.status_code == 403:
            self._tokens = self._refresh_tokens()
            response = super()._make_request(
                method,
                url,
                payload,
                {
                    **headers,
                    **{
                        "Authorization": self._tokens["accessToken"]
                    }
                }
            )
        return response

    def _make_request(self, method, url, payload, headers):
        if not self._tokens:
            self._tokens = self._authenticate()
        return self._make_authenticated_request(method, url, payload, headers)
