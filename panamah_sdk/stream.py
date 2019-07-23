import time
from .models.base import Model
from .processor import BatchProcessor


class PanamahStream():
    class _PanamahStream():
        def __init__(self, authorization_token, secret, assinante_id):
            self.authorization_token = authorization_token
            self.secret = secret
            self.assinante_id = assinante_id
            self.processor = BatchProcessor(
                authorization_token, secret, assinante_id)
            self.processor.start()

        def is_acceptable_model(self, model):
            return hasattr(model, 'name') and model.name != 'ASSINANTE'

        def save(self, model, assinanteId=None):
            if isinstance(model, Model) and self.is_acceptable_model(model):
                self.processor.save(model, assinanteId)
            else:
                raise ValueError('model deve ser um modelo valido do Panamah')

        def delete(self, model, assinanteId=None):
            if isinstance(model, Model)  and self.is_acceptable_model(model):
                self.processor.delete(model, assinanteId)
            else:
                raise ValueError('model deve ser um modelo valido do Panamah')

        def flush(self):
            self.processor.flush()

    instance = None

    def __init__(self, authorization_token, secret, assinante_id='*'):
        if self.instance is None:
            self.instance = PanamahStream._PanamahStream(
                authorization_token, secret, assinante_id)
        PanamahStream.authorization_token = authorization_token
        PanamahStream.secret = secret
        PanamahStream.assinante_id = assinante_id

    def __getattr__(self, name):
        return getattr(self.instance, name)
