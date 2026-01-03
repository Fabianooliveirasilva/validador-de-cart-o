"""CLI simples para consultar a bandeira de um número de cartão"""

import argparse

from .detector import detect_brand, is_luhn_valid


def main():
    parser = argparse.ArgumentParser(description="Detecta a bandeira de um cartão")
    parser.add_argument(
        "number",
        help="Número do cartão (pode ter espaços ou hífens)",
    )
    parser.add_argument(
        "--require-luhn",
        action="store_true",
        help="Retornar Unknown se Luhn inválido",
    )
    args = parser.parse_args()

    brand = detect_brand(args.number, validate_luhn=args.require_luhn)
    luhn_ok = is_luhn_valid(args.number)

    print(f"Brand: {brand}")
    print(f"Luhn válido: {luhn_ok}")


if __name__ == "__main__":
    main()
