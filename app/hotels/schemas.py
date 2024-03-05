from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict


class SHotel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int


class SHotelInfo(SHotel):
    rooms_left: int
