import random
from typing import Optional

from ..model import Sensor, UnitProperty

DEFAULT_RANGES = {
    "celsius": (15.0, 45.0),
    "fahrenheit": (59.0, 113.0),
    "percent": (0.0, 100.0),
    "lux": (0.0, 100000.0),
    "ppm": (300.0, 5000.0),
    "hPa": (950.0, 1050.0),
}
DEFAULT_RANGE = (0.0, 100.0)


def _get_unit(sensor: Sensor) -> str:
    for prop in sensor.properties:
        if isinstance(prop, UnitProperty):
            return prop.value
    return ""


def generate_readings(
    sensors: dict[str, Sensor],
    overrides: Optional[dict[str, float]] = None,
) -> dict[str, float]:
    readings: dict[str, float] = {}
    for name, sensor in sensors.items():
        if overrides and name in overrides:
            readings[name] = overrides[name]
        else:
            unit = _get_unit(sensor)
            lo, hi = DEFAULT_RANGES.get(unit, DEFAULT_RANGE)
            readings[name] = round(random.uniform(lo, hi), 2)
    return readings
