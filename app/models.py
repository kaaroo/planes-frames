from tortoise import fields, models

from app.settings import MIN_SPEED_KM_H, MIN_LONGITUDE, MAX_LONGITUDE, MIN_LATITUDE, MAX_LATITUDE, MIN_ALT_METERS
from app.validator import validate_icao


class Plane(models.Model):
    """
    The Plane model
    """
    icao = fields.CharField(primary_key=True, max_length=4, validators=[validate_icao])

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>" + str({
            "icao": self.icao,
        })


class PlaneFrame(models.Model):
    """
    The PlaneFrame model
    """
    id = fields.IntField(primary_key=True)
    plane = fields.ForeignKeyField("models.Plane", related_name="frames")
    speed = fields.FloatField(min=MIN_SPEED_KM_H)
    lon = fields.FloatField(min=MIN_LONGITUDE, max=MAX_LONGITUDE)
    lat = fields.FloatField(min=MIN_LATITUDE, max=MAX_LATITUDE)
    alt = fields.IntField(min=MIN_ALT_METERS)
    timestamp = fields.DatetimeField()

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>" + str({
            "id": id,
            "icao": self.plane_id,
            "timestamp": self.timestamp,
        })
