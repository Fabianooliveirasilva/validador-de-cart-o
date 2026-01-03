# API / Referência

Módulos principais:

- `validador_bandeiras.detect_brand(number: str, validate_luhn: bool = False) -> Optional[str]`

  - Detecta a bandeira com base no número (retorna nome da bandeira ou `None`/`"Unknown"`).
  - `validate_luhn=True` faz a função retornar `None` se o número não passar no Luhn.

- `validador_bandeiras.is_luhn_valid(number: str) -> bool`

  - Retorna `True` se o número passar na verificação de Luhn.

- `validador_bandeiras.clean_number(number: str) -> str`
  - Remove espaços e caracteres não-numéricos.

Padrões suportados (atual): Visa, MasterCard, American Express, Discover, JCB, Diners Club.

Exemplo de uso em código:

```python
from validador_bandeiras import detect_brand, is_luhn_valid

num = "378282246310005"
print(detect_brand(num))  # -> "American Express"
print(is_luhn_valid(num))  # -> True
```
