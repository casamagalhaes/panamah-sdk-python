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
from panamah_sdk.exceptions import NotFoundException
from panamah_sdk.models.definitions import PanamahAssinante

admin = PanamahAdmin()

try:
    assinante = admin.get_assinante('21705632000120')
    print(assinante)
except NotFoundException:
        #instanciando um modelo de assinante
        assinante = PanamahAssinante(
            id='21705632000120',
            fantasia='Supermercado Exemplo',
            nome='Supermercado Exemplo Ltda',
            bairro='Rua Poebla',
            cidade='Caucaia',
            uf='CE'
        )
        #criando o assinante no Panamah
        created_assinante = admin.create_assinante(assinante)
        print(created_assinante)
```

## Exemplo de uso da API de streaming