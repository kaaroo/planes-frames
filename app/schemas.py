import re

from pydantic import BaseModel, field_validator, Field

from app.config import MIN_SPEED_KM_H, MAX_SPEED_KM_H, MIN_LONGITUDE, MAX_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE


class PlaneDataFrame(BaseModel):
    icao: str
    speed: float = Field(None, ge=MIN_SPEED_KM_H, le=MAX_SPEED_KM_H)
    longitude: float = Field(None, ge=MIN_LONGITUDE, le=MAX_LONGITUDE)
    latitude: float = Field(None, ge=MIN_LATITUDE, le=MAX_LATITUDE)
    alt: int = Field(None, ge=0)
    timestamp: str

    @field_validator("icao")
    def icao_match(cls, v: str) -> str:
        if re.match(r':[A-Z]+$', v):
            raise ValueError("Value (icao) can have only uppercase letters")
        if len(v) != 4:
            raise ValueError("Value (icao) must be of length 4")

        return v

    # TODO validate timestamp?
    pass
