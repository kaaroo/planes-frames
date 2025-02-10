import re
from datetime import datetime

from pydantic import BaseModel, field_validator, Field
from pydantic_core import ValidationError

from app.settings import MAX_SPEED_KM_H, MIN_SPEED_KM_H, MIN_LONGITUDE, MAX_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE


class Plane(BaseModel):
    icao: str


class PlaneDataFrame(BaseModel):
    icao: str
    speed: float = Field(None, ge=MIN_SPEED_KM_H, le=MAX_SPEED_KM_H)
    lon: float = Field(None, ge=MIN_LONGITUDE, le=MAX_LONGITUDE)
    lat: float = Field(None, ge=MIN_LATITUDE, le=MAX_LATITUDE)
    alt: int = Field(None, ge=0)
    timestamp: datetime

    @field_validator("icao")
    def icao_match(cls, v: str) -> str:
        validate_icao(v)
        return v


def validate_icao(value: str) -> None:
    if re.match(r':[A-Z]+$', value):
        raise ValidationError("Value (icao) can have only uppercase letters")
    if len(value) != 4:
        raise ValidationError("Value (icao) must be of length 4")
