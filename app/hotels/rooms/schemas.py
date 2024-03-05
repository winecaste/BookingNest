from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    services: List[str]
    price: int
    quantity: int
    image_id: int


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int
