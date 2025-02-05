from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityCreate):
    pass


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: int


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureUpdate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True
