"""
validator.py
------------
Lógica pura para identificação de bandeira e validação de número de cartão de crédito.
Sem dependências externas — apenas Python stdlib.
"""

from typing import Optional


# ---------------------------------------------------------------------------
# Regras de detecção de bandeira
# Cada entrada: (nome, função_de_verificação)
# A função recebe o número (string de dígitos) e retorna True se corresponde.
# A ordem importa: regras mais específicas devem vir antes das mais genéricas.
# ---------------------------------------------------------------------------

def _starts_with(number: str, prefixes) -> bool:
    """Retorna True se o número começa com algum dos prefixos fornecidos."""
    if isinstance(prefixes, (str, int)):
        prefixes = [str(prefixes)]
    return any(number.startswith(str(p)) for p in prefixes)


def _in_range(number: str, length: int, start: int, end: int) -> bool:
    """Retorna True se os primeiros `length` dígitos estão no intervalo [start, end]."""
    if len(number) < length:
        return False
    prefix = int(number[:length])
    return start <= prefix <= end


BRAND_RULES = [
    # American Express: começa com 34 ou 37, 15 dígitos
    ("American Express", lambda n: _starts_with(n, ["34", "37"]) and len(n) == 15),

    # Diners Club: começa com 300-305, 36 ou 38, 14 dígitos
    ("Diners Club", lambda n: (
        (_in_range(n, 3, 300, 305) or _starts_with(n, ["36", "38"])) and len(n) == 14
    )),

    # EnRoute: começa com 2014 ou 2149, 15 dígitos
    ("EnRoute", lambda n: _starts_with(n, ["2014", "2149"]) and len(n) == 15),

    # Voyager: começa com 8699, 15 dígitos
    ("Voyager", lambda n: _starts_with(n, ["8699"]) and len(n) == 15),

    # JCB: 3528–3589, 16 dígitos
    ("JCB", lambda n: _in_range(n, 4, 3528, 3589) and len(n) == 16),

    # HiperCard: começa com 6062 ou 3841, 16 dígitos
    ("HiperCard", lambda n: _starts_with(n, ["6062", "3841"]) and len(n) == 16),

    # Discover: 6011, 622126–622925, 644–649, 65 — 16 dígitos
    ("Discover", lambda n: (
        (
            _starts_with(n, ["6011"])
            or _in_range(n, 6, 622126, 622925)
            or _in_range(n, 3, 644, 649)
            or _starts_with(n, ["65"])
        ) and len(n) == 16
    )),

    # Aura: começa com 50, 16 dígitos
    ("Aura", lambda n: _starts_with(n, ["50"]) and len(n) == 16),

    # MasterCard: 51–55 ou 2221–2720, 16 dígitos
    ("MasterCard", lambda n: (
        (_in_range(n, 2, 51, 55) or _in_range(n, 4, 2221, 2720)) and len(n) == 16
    )),

    # Visa: começa com 4, 13 ou 16 dígitos
    ("Visa", lambda n: _starts_with(n, ["4"]) and len(n) in (13, 16)),
]


def detect_brand(number: str) -> Optional[str]:
    """
    Identifica a bandeira do cartão com base no número fornecido.

    Args:
        number: String contendo apenas dígitos do número do cartão.

    Returns:
        Nome da bandeira (str) ou None se não reconhecida.
    """
    digits = "".join(filter(str.isdigit, number))
    if not digits:
        return None
    for brand_name, rule in BRAND_RULES:
        if rule(digits):
            return brand_name
    return None


def luhn_check(number: str) -> bool:
    """
    Valida um número de cartão usando o algoritmo de Luhn.

    Args:
        number: String contendo apenas dígitos do número do cartão.

    Returns:
        True se o número passa na validação de Luhn, False caso contrário.
    """
    digits = "".join(filter(str.isdigit, number))
    if not digits or len(digits) < 2:
        return False

    total = 0
    reverse = digits[::-1]

    for i, ch in enumerate(reverse):
        n = int(ch)
        if i % 2 == 1:          # posições ímpares (0-indexed) são dobradas
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0


def validate_card(number: str) -> dict:
    """
    Retorna um dicionário com bandeira detectada, validade Luhn e número limpo.

    Args:
        number: Número do cartão (pode conter espaços ou hífens).

    Returns:
        {
            "digits": str,          # apenas os dígitos
            "brand": str | None,    # nome da bandeira ou None
            "luhn_valid": bool,     # resultado do algoritmo de Luhn
            "length": int           # quantidade de dígitos
        }
    """
    digits = "".join(filter(str.isdigit, number))
    return {
        "digits": digits,
        "brand": detect_brand(digits),
        "luhn_valid": luhn_check(digits),
        "length": len(digits),
    }
