from pydantic import (
    BaseModel,
)
from pydantic_settings import BaseSettings


class Chips(BaseModel):
    extra_drs: bool = False


class Settings(BaseSettings):
    chips: Chips = Chips()
    qualifying_only: bool = False


SETTINGS = Settings()
