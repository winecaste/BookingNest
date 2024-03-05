from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingInfo, SNewBooking
from app.exceptions import (
    DateFromCannotBeAfterDateTo,
    DaysHasBeenExceeded,
    RoomCannotBeBooked,
)

from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingInfo]:
    bookings = await BookingDAO.find_all_with_images(user.id)
    return bookings


@router.delete("/{booking_id}")
async def remove_booking(
    booking_id: int, current_user: Users = Depends(get_current_user)
):  # -> list[SBooking]:
    await BookingDAO.delete(id=booking_id, user_id=current_user.id)


@router.post("", status_code=201)
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user),
):
    if (booking.date_to - booking.date_from).days > 31:
        raise DaysHasBeenExceeded
    if booking.date_from > booking.date_to:
        raise DateFromCannotBeAfterDateTo
    booking = await BookingDAO.add(
        user.id,
        booking.room_id,
        booking.date_from,
        booking.date_to
    )
    if not booking:
        raise RoomCannotBeBooked
    all_bookings = await BookingDAO.find_all_with_images(user.id)
    booking_dict = parse_obj_as(SBookingInfo, all_bookings[-1]).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict
