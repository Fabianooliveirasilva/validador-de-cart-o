"""Padrões e utilitários para identificação de bandeiras"""

import re

# Padrões regex simples para algumas bandeiras
BRAND_PATTERNS = {
    "Visa": re.compile(r"^4\d{12}(?:\d{3}){0,2}$"),  # 13, 16, 19 dígitos
    "American Express": re.compile(r"^3[47]\d{13}$"),  # 15 dígitos
    "Diners Club": re.compile(r"^3(?:0[0-5]|[68]\d)\d{11}$"),
    "JCB": re.compile(r"^35(?:2[89]|[3-8]\d)\d{12}$"),
}


# Regras programáticas para MasterCard e Discover (prefixos/ranges)
def is_mastercard(number: str) -> bool:
    if len(number) != 16:
        return False
    first_two = int(number[:2])
    first_six = int(number[:6])
    if 51 <= first_two <= 55:
        return True
    if 222100 <= first_six <= 272099:
        return True
    return False


def is_discover(number: str) -> bool:
    if len(number) not in (16, 19):
        return False
    if number.startswith("6011") or number.startswith("65"):
        return True
    first_three = int(number[:3])
    if 644 <= first_three <= 649:
        return True
    first_six = int(number[:6])
    if 622126 <= first_six <= 622925:
        return True
    return False
