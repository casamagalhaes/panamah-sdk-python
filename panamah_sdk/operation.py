from .models.base import Model


class Operation():
    def __init__(self, data, tipo, op, assinanteId, id):
        self.id = id
        self.data = data
        self.op = op
        self.tipo = tipo
        self.assinanteId = assinanteId

    @classmethod
    def create_from_model(cls, op, model, assinanteId):
        data = model.json()
        tipo = model.name
        id = model.id
        return Operation(data, tipo, op, assinanteId, id)

class Update(Operation):
    def __init__(self, data, tipo, op, assinanteId, id):
        super().__init__(data, tipo, 'update', assinanteId, id)

    @classmethod
    def create_from_model(cls, model, assinanteId):
        return super().create_from_model('update', model, assinanteId)

class Delete(Operation):
    def __init__(self, data, tipo, op, assinanteId, id):
        super().__init__(data, tipo, 'delete', assinanteId, id)

    @classmethod
    def create_from_model(cls, model, assinanteId):
        return super().create_from_model('delete', model, assinanteId)
