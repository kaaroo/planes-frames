from tortoise import fields, models

from app.config import MIN_SPEED_KM_H, MIN_LONGITUDE, MAX_LONGITUDE, MAX_LATITUDE, MIN_LATITUDE, \
    MIN_ALT_METERS
from app.validator import validate_icao


class Plane(models.Model):
    """
    The Plane model
    """
    icao = fields.CharField(primary_key=True, max_length=4, validators=validate_icao)


class PlaneFrame(models.Model):
    """
    The PlaneFrame model
    """
    id = fields.IntField(primary_key=True)
    plane = fields.ForeignKeyRelation[Plane] = fields.ForeignKeyField(
        "models.Plane", related_name="frames"
    )
    speed = fields.FloatField(min=MIN_SPEED_KM_H)
    lon = fields.FloatField(min=MIN_LONGITUDE, max=MAX_LONGITUDE)
    lat = fields.FloatField(min=MIN_LATITUDE, max=MAX_LATITUDE)
    alt = fields.IntField(min=MIN_ALT_METERS)
    timestamp = fields.DatetimeField()
