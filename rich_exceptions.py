from rich.pretty import pprint

try:
    1 / 0
except Exception as exc:
    pprint(exc)
