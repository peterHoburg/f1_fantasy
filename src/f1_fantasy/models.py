from enum import Enum

from pydantic import BaseModel, ConfigDict


class DriversEnum(Enum):
    MAX = "MAX"
    CHARLES = "CHARLES"
    GEORGE = "GEORGE"
    CARLOS = "CARLOS"
    SERGIO = "SERGIO"
    FERNANDO = "FERNANDO"
    LANDO = "LANDO"
    OSCAR = "OSCAR"
    LEWIS = "LEWIS"
    NICO = "NICO"
    YUKI = "YUKI"
    LANCE = "LANCE"
    ALEXANDER = "ALEXANDER"
    DANIEL = "DANIEL"
    KEVIN = "KEVIN"
    VALTTERI = "VALTTERI"
    ZHOU = "ZHOU"
    LOGAN = "LOGAN"
    ESTEBAN = "ESTEBAN"
    PIERRE = "PIERRE"


class ConstructorsEnum(Enum):
    RED_BULL = "RED_BULL"
    MCLAREN = "MCLAREN"
    MERCEDES = "MERCEDES"
    FERRARI = "FERRARI"
    ASTON_MARTIN = "ASTON_MARTIN"
    RB = "RB"
    ALPINE = "ALPINE"
    WILLIAMS = "WILLIAMS"
    SAUBER = "SAUBER"
    HAAS = "HAAS"


class DriverPriceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: DriversEnum
    price: float


class ConstructorPriceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: ConstructorsEnum
    price: float


class FinishingPositionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    drivers: list[DriversEnum]


class SpecialPoints(BaseModel):
    fastest_lap: DriversEnum | None = None
    driver_of_the_day: DriversEnum | None = None
    fastest_pitstop: ConstructorsEnum | None = None
    second_fastest_pitstop: ConstructorsEnum | None = None
    third_fastest_pitstop: ConstructorsEnum | None = None
