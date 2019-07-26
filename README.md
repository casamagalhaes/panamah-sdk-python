## Requisitos mínimos

- Python >= 3.4

## Instalação

1. Execute o comando

   ```bash
   pip install panamah-sdk-python
   ```

2. Utilize as APIs e modelos através do
   ```python
   from panamah_sdk.stream import PanamahStream
   from panamah_sdk.admin import PanamahAdmin
   #Todas as definições de modelos
   from panamah_sdk.models.definitions import *
   #Só algumas
   from panamah_sdk.models.definitions import PanamahProduto, PanamahSecao
   ```

## Visão geral

[Leia mais aqui](https://github.com/casamagalhaes/panamah-sdk-python/wiki/Visão-geral)

## Exemplo de uso da API administrativa

```python
from panamah_sdk.admin import PanamahAdmin

admin = PanamahAdmin(authorization_token=)

try:
    assinante = admin.get_assinante('18475929000132')
except Exception as e:
    if (e.name === 'PanamahNotFoundError') {
        #instanciando um modelo de assinante
        assinante = PanamahAssinante(
            id='18475929000132',
            fantasia='Supermercado Exemplo',
            nome='Supermercado Exemplo Ltda',
            bairro='Rua Poebla',
            cidade='Caucaia',
            uf='CE'
        )
        #criando o assinante no Panamah
        admin.create_assinante(assinante)
    }
}
```
