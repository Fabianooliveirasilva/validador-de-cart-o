"""Lógica para limpar número, validar Luhn e detectar a bandeira"""

import re
from typing import Optional

from .patterns import BRAND_PATTERNS, is_discover, is_mastercard


def clean_number(number: str) -> str:
    """Remove espaços e hífens"""
    return re.sub(r"[^0-9]", "", number)


def is_luhn_valid(number: str) -> bool:
    """Verifica o algoritmo de Luhn"""
    s = clean_number(number)
    if not s.isdigit() or len(s) < 12:
        return False
    total = 0
    reverse_digits = s[::-1]
    for i, ch in enumerate(reverse_digits):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def detect_brand(number: str, validate_luhn: bool = False) -> Optional[str]:
    """Detecta a bandeira com base no número. Retorna None se indefinido."""
    s = clean_number(number)
    if not s:
        return None

    # Opção: checar Luhn primeiro
    if validate_luhn and not is_luhn_valid(s):
        return None

    # Checar padrões simples
    for brand, pattern in BRAND_PATTERNS.items():
        if pattern.match(s):
            return brand

    # Regras programáticas
    if is_mastercard(s):
        return "MasterCard"
    if is_discover(s):
        return "Discover"

    return "Unknown"
