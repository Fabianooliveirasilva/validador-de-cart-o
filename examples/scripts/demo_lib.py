"""Demo rápido de uso da biblioteca `validador_bandeiras`.

Uso:
    python examples/scripts/demo_lib.py              # roda exemplos internos
    python examples/scripts/demo_lib.py 4111111111111111  # testa um número específico
"""

import sys

from validador_bandeiras import detect_brand, is_luhn_valid

examples = [
    "4111111111111111",
    "5555555555554444",
    "378282246310005",
    "6011111111111117",
    "3530111333300000",
    "30569309025904",
]

if len(sys.argv) > 1:
    examples = sys.argv[1:]

for number in examples:
    brand = detect_brand(number)
    luhn = is_luhn_valid(number)
    print(f"{number} -> brand: {brand}, luhn_valid: {luhn}")
