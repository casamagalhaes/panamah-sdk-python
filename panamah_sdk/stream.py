from .models.base import Model
from .processor import Processor


class PanamahStream():
    class _PanamahStream():
        def __init__(self, authorization_token, secret, assinante_id):
            self.authorization_token = authorization_token
            self.secret = secret
            self.assinante_id = assinante_id

        def save(self, model):
            if isinstance(model, Model):
                model.validate()
            else:
                raise ValueError('model deve ser um modelo valido do Panamah')

        def delete(self, model):
            if isinstance(model, Model):
                pass
            else:
                raise ValueError('model deve ser um modelo valido do Panamah')

    instance = _PanamahStream(authorization_token=None,
                              secret=None, assinante_id='*')

    def __init__(self, authorization_token, secret, assinante_id='*'):
        PanamahStream.authorization_token = authorization_token
        PanamahStream.secret = secret
        PanamahStream.assinante_id = assinante_id

    def __getattr__(self, name):
        return getattr(self.instance, name)
