from .base import Model, StringField, NumberField, BooleanField, DateField, ObjectField, StringListField, ObjectListField


class PanamahAssinante(Model):
    name = 'ASSINANTE'
    schema = {
        'id': StringField(required=True),
        'nome': StringField(required=True),
        'fantasia': StringField(required=True),
        'ramo': StringField(required=True),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'revenda_id': StringField(required=False),
        'bairro': StringField(required=True),
        'softwares_ativos': StringListField(required=True, allowedValues=['MILENIO', 'SYSPDV', 'VAREJOFACIL', 'SYSPDVWEB', 'EASYASSIST', 'SYSPDV_APP', 'COLETOR']),
        'softwares_em_contratos_de_manutencao': StringListField(required=True, allowedValues=['MILENIO', 'SYSPDV', 'VAREJOFACIL', 'SYSPDVWEB', 'EASYASSIST', 'SYSPDV_APP', 'COLETOR']),
        'series': StringListField(required=False),
        'ativo': BooleanField(required=True, default=True)
    }


class PanamahRevenda(Model):
    name = 'REVENDA'
    schema = {
        'id': StringField(required=True),
        'nome': StringField(required=True),
        'fantasia': StringField(required=True),
        'ramo': StringField(required=True),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'bairro': StringField(required=True)
    }


class PanamahSecao(Model):
    name = 'SECAO'
    schema = {
        'id': StringField(required=True),
        'codigo': StringField(required=True),
        'descricao': StringField(required=True)
    }


class PanamahGrupo(Model):
    name = 'GRUPO'
    schema = {
        'id': StringField(required=True),
        'codigo': StringField(required=True),
        'descricao': StringField(required=True),
        'secao_id': StringField(required=True)
    }


class PanamahSubgrupo(Model):
    name = 'SUBGRUPO'
    schema = {
        'id': StringField(required=True),
        'codigo': StringField(required=True),
        'descricao': StringField(required=True),
        'secao_id': StringField(required=True),
        'grupo_id': StringField(required=True)
    }


class PanamahHolding(Model):
    name = 'HOLDING'
    schema = {
        'id': StringField(required=True),
        'descricao': StringField(required=True)
    }


class PanamahLoja(Model):
    name = 'LOJA'
    schema = {
        'ativa': BooleanField(required=True),
        'id': StringField(required=True),
        'descricao': StringField(required=True),
        'numero_documento': StringField(required=True),
        'matriz': BooleanField(required=True),
        'holding_id': StringField(required=True),
        'ramo': StringField(required=True),
        'logradouro': StringField(required=False),
        'numero': StringField(required=False),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'bairro': StringField(required=True),
        'cep': StringField(required=False),
        'distrito': StringField(required=False),
        'complemento': StringField(required=False),
        'telefone': StringField(required=False),
        'qtd_checkouts': NumberField(required=False),
        'area_m_2': NumberField(required=False),
        'qtd_funcionarios': NumberField(required=False)
    }


class PanamahMeta(Model):
    name = 'META'
    schema = {
        'id': StringField(required=True),
        'mes': NumberField(required=True),
        'ano': NumberField(required=True),
        'loja_id': StringField(required=True),
        'secao_id': StringField(required=True),
        'valor': NumberField(required=True)
    }


class PanamahFormaPagamento(Model):
    name = 'FORMA_PAGAMENTO'
    schema = {
        'id': StringField(required=True),
        'descricao': StringField(required=True)
    }


class PanamahFuncionario(Model):
    name = 'FUNCIONARIO'
    schema = {
        'data_nascimento': DateField(required=False),
        'id': StringField(required=True),
        'login': StringField(required=False),
        'nome': StringField(required=True),
        'numero_documento': StringField(required=False),
        'ativo': BooleanField(required=True),
        'senha': StringField(required=False),
        'loja_ids': StringListField(required=False)
    }


class PanamahAcesso(Model):
    name = 'ACESSO'
    schema = {
        'id': StringField(required=True),
        'funcionario_ids': StringListField(required=True)
    }


class PanamahCliente(Model):
    name = 'CLIENTE'
    schema = {
        'id': StringField(required=True),
        'nome': StringField(required=True),
        'numero_documento': StringField(required=True),
        'ramo': StringField(required=True),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'bairro': StringField(required=True)
    }


class PanamahFornecedor(Model):
    name = 'FORNECEDOR'
    schema = {
        'id': StringField(required=True),
        'nome': StringField(required=True),
        'numero_documento': StringField(required=True),
        'ramo': StringField(required=True),
        'uf': StringField(required=True),
        'cidade': StringField(required=True),
        'bairro': StringField(required=True)
    }


class PanamahProdutoFornecedor(Model):
    schema = {
        'id': StringField(required=True),
        'principal': BooleanField(required=True)
    }


class PanamahProdutoComposicaoItem(Model):
    schema = {
        'produto_id': StringField(required=True),
        'quantidade': NumberField(required=True)
    }


class PanamahProdutoComposicao(Model):
    schema = {
        'itens': ObjectListField(required=False, object_class=PanamahProdutoComposicaoItem),
        'quantidade': NumberField(required=True)
    }


class PanamahProduto(Model):
    name = 'PRODUTO'
    schema = {
        'composicao': ObjectField(required=False, object_class=PanamahProdutoComposicao),
        'tipo_composicao': StringField(required=False),
        'descricao': StringField(required=True),
        'data_inclusao': DateField(required=False),
        'finalidade': StringField(required=False),
        'ativo': BooleanField(required=False),
        'grupo_id': StringField(required=False),
        'id': StringField(required=True),
        'peso_variavel': BooleanField(required=False),
        'quantidade_itens_embalagem': NumberField(required=False),
        'secao_id': StringField(required=True),
        'subgrupo_id': StringField(required=False),
        'fornecedores': ObjectListField(required=False, object_class=PanamahFornecedor)
    }


class PanamahEan(Model):
    name = 'EAN'
    schema = {
        'id': StringField(required=True),
        'produto_id': StringField(required=True),
        'tributado': BooleanField(required=False)
    }


class PanamahTrocaFormaPagamento(Model):
    name = 'TROCA_FORMA_PAGAMENTO'
    schema = {
        'autorizador_id': StringField(required=False),
        'data': DateField(required=True),
        'forma_pagamento_destino_id': StringField(required=True),
        'forma_pagamento_origem_id': StringField(required=True),
        'id': StringField(required=True),
        'loja_id': StringField(required=True),
        'venda_id': StringField(required=False),
        'operador_id': StringField(required=False),
        'sequencial_pagamento': StringField(required=True),
        'valor': NumberField(required=True),
        'valor_contra_vale_ou_troco': NumberField(required=False)
    }


class PanamahTrocaDevolucaoItem(Model):
    schema = {
        'desconto': NumberField(required=False),
        'produto_id': StringField(required=True),
        'quantidade': NumberField(required=True),
        'valor_total': NumberField(required=True),
        'valor_unitario': NumberField(required=True),
        'vendedor_id': StringField(required=False)
    }


class PanamahTrocaDevolucao(Model):
    name = 'TROCA_DEVOLUCAO'
    schema = {
        'autorizador_id': StringField(required=False),
        'data': DateField(required=True),
        'venda_id': StringField(required=False),
        'id': StringField(required=True),
        'itens': ObjectListField(required=True, object_class=PanamahTrocaDevolucaoItem),
        'loja_id': StringField(required=True),
        'numero_caixa': StringField(required=False),
        'operador_id': StringField(required=False),
        'sequencial': StringField(required=False),
        'valor': NumberField(required=True),
        'vendedor_id': StringField(required=False)
    }


class PanamahEventoCaixaValoresDeclarados(Model):
    schema = {
        'forma_pagamento_id': StringField(required=True),
        'valor': NumberField(required=True)
    }


class PanamahEventoCaixa(Model):
    name = 'EVENTO_CAIXA'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True),
        'numero_caixa': StringField(required=True),
        'funcionario_id': StringField(required=False),
        'data_hora': DateField(required=True),
        'tipo': StringField(required=True, allowedValues=['ABERTURA', 'FECHAMENTO', 'ENTRADA_OPERADOR', 'SAIDA_OPERADOR']),
        'valores_declarados': ObjectListField(required=False, object_class=PanamahEventoCaixaValoresDeclarados)
    }


class PanamahVendaPagamento(Model):
    schema = {
        'forma_pagamento_id': StringField(required=True),
        'sequencial': StringField(required=True),
        'valor': NumberField(required=True)
    }


class PanamahVendaItem(Model):
    schema = {
        'acrescimo': NumberField(required=False),
        'desconto': NumberField(required=False),
        'efetivo': BooleanField(required=True, default=True),
        'funcionario_id': StringField(required=False),
        'preco': NumberField(required=True),
        'produto_id': StringField(required=True),
        'codigo_registrado': StringField(required=False),
        'promocao': BooleanField(required=False),
        'quantidade': NumberField(required=True),
        'servico': NumberField(required=False),
        'valor_total': NumberField(required=True),
        'valor_unitario': NumberField(required=True),
        'tipo_preco': StringField(required=True),
        'custo': NumberField(required=False),
        'markup': NumberField(required=False),
        'lucro': NumberField(required=False)
    }


class PanamahVenda(Model):
    name = 'VENDA'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True),
        'cliente_id': StringField(required=False),
        'funcionario_id': StringField(required=False),
        'data': DateField(required=True),
        'data_hora_inicio': DateField(required=False),
        'data_hora_fim': DateField(required=False),
        'data_hora_venda': DateField(required=True),
        'desconto': NumberField(required=False),
        'efetiva': BooleanField(required=True, default=True),
        'quantidade_itens': NumberField(required=True),
        'quantidade_itens_cancelados': NumberField(required=False),
        'sequencial': StringField(required=True),
        'servico': NumberField(required=False),
        'tipo_desconto': StringField(required=False),
        'tipo_preco': StringField(required=True),
        'valor': NumberField(required=True),
        'valor_itens_cancelados': NumberField(required=False),
        'acrescimo': NumberField(required=False),
        'numero_caixa': StringField(required=False),
        'itens': ObjectListField(required=True, object_class=PanamahVendaItem),
        'pagamentos': ObjectListField(required=True, object_class=PanamahVendaPagamento)
    }


class PanamahCompraItem(Model):
    schema = {
        'acrescimo': NumberField(required=False),
        'desconto': NumberField(required=False),
        'produto_id': StringField(required=True),
        'quantidade': NumberField(required=True),
        'valor_total': NumberField(required=True),
        'valor_unitario': NumberField(required=True)
    }


class PanamahCompra(Model):
    name = 'COMPRA'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True),
        'fornecedor_id': StringField(required=False),
        'funcionario_id': StringField(required=False),
        'data_entrada': DateField(required=True),
        'data_emissao': DateField(required=True),
        'data_hora_compra': DateField(required=True),
        'desconto': NumberField(required=False),
        'efetiva': BooleanField(required=True, default=True),
        'quantidade_itens': NumberField(required=True),
        'tipo_desconto': StringField(required=False),
        'valor': NumberField(required=True),
        'acrescimo': NumberField(required=False),
        'itens': ObjectListField(required=True, object_class=PanamahCompraItem)
    }


class PanamahLocalEstoque(Model):
    name = 'LOCAL_ESTOQUE'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True),
        'descricao': StringField(required=True),
        'disponivel_para_venda': BooleanField(required=True)
    }


class PanamahEstoqueMovimentacao(Model):
    name = 'ESTOQUE_MOVIMENTACAO'
    schema = {
        'id': StringField(required=True),
        'local_estoque_id': StringField(required=True),
        'data_hora': DateField(required=True),
        'produto_id': StringField(required=True),
        'quantidade': NumberField(required=True),
        'custo': NumberField(required=True),
        'preco': NumberField(required=True),
        'markup': NumberField(required=False)
    }


class PanamahTituloPagarPagamento(Model):
    schema = {
        'data_hora': DateField(required=True),
        'valor': NumberField(required=True)
    }


class PanamahTituloPagar(Model):
    name = 'TITULO_PAGAR'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True),
        'fornecedor_id': StringField(required=True),
        'documento': StringField(required=True),
        'valor_nominal': NumberField(required=True),
        'valor_juros': NumberField(required=True),
        'valor_multa': NumberField(required=True),
        'valor_devido': NumberField(required=True),
        'valor_pago': NumberField(required=True),
        'data_emissao': DateField(required=True),
        'data_vencimento': DateField(required=True),
        'pagamentos': ObjectListField(required=True, object_class=PanamahTituloPagarPagamento)
    }


class PanamahTituloReceberPagamento(Model):
    schema = {
        'data_hora': DateField(required=True),
        'valor': NumberField(required=True)
    }


class PanamahTituloReceber(Model):
    name = 'TITULO_RECEBER'
    schema = {
        'id': StringField(required=True),
        'loja_id': StringField(required=True),
        'cliente_id': StringField(required=True),
        'documento': StringField(required=True),
        'valor_nominal': NumberField(required=True),
        'valor_juros': NumberField(required=True),
        'valor_multa': NumberField(required=True),
        'valor_devido': NumberField(required=True),
        'valor_pago': NumberField(required=True),
        'data_emissao': DateField(required=True),
        'data_vencimento': DateField(required=True),
        'pagamentos': ObjectListField(required=True, object_class=PanamahTituloReceberPagamento)
    }


def from_json(name, json):
    for cls_name in globals():
        cls = globals()[cls_name]
        if type(cls) is type(object) and issubclass(cls, Model) and hasattr(cls, 'name') and cls.name == name:
            return cls.from_json(json)
    return None
