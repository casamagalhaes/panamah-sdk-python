from .base import *


class Assinante(Model):
    schema = {
        'nome': StringField(required=True),
        'ativo': BooleanField(required=True, default=True),
        'softwaresAtivos': StringListField(allowedValues=['MILENIO', 'SYSPDV', 'VAREJOFACIL', 'SYSPDVWEB', 'EASYASSIST', 'SYSPDV_APP', 'COLETOR'], required=True)
    }


class ProdutoComposicaoItem(Model):
    schema = {
        'produtoId': StringField(required=True)
    }


class ProdutoComposicao(Model):
    schema = {
        'itens': ObjectListField(object_class=ProdutoComposicaoItem, required=True),
        'quantidade': NumberField(required=True)
    }


class Produto(Model):
    schema = {
        'tipoComposicao': StringField(required=True),
        'composicao': ObjectField(object_class=ProdutoComposicao, required=True)
    }
