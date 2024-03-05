from datetime import date, datetime, timedelta
from typing import List, Optional, Annotated
import asyncio
from fastapi import APIRouter, Query, Form
from fastapi_cache.decorator import cache


from app.exceptions import DateFromCannotBeAfterDateTo, DaysHasBeenExceeded
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel, SHotelInfo

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomInfo

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise DaysHasBeenExceeded
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}", include_in_schema=True)
async def get_hotel_by_id(
        hotel_id: int,
):
    return await HotelDAO.find_one_or_none(id=hotel_id)


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SRoomInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise DaysHasBeenExceeded
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    return rooms