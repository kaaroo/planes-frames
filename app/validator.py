import re

from pydantic_core._pydantic_core import ValidationError


def validate_icao(value: str) -> None:
    if re.match(r':[A-Z]+$', value):
        raise ValidationError("Value (icao) can have only uppercase letters")
    if len(value) != 4:
        raise ValidationError("Value (icao) must be of length 4")
