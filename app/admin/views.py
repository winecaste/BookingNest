from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    name = "User"
    column_list = [Users.id, Users.email, Users.booking]
    icon = "fa-solid fa-user"
    column_details_exclude_list = [Users.hashed_password]


class BookingsAdmin(ModelView, model=Bookings):
    name = "Booking"
    column_list = '__all__'
    icon = "fa-solid fa-book"


class HotelsAdmin(ModelView, model=Hotels):
    name = "Hotel"
    column_list = [c.name for c in Hotels.__table__.c]
    column_list += [Hotels.rooms]
    icon = "fa-solid fa-hotel"
    can_delete = False


class RoomsAdmin(ModelView, model=Rooms):
    name = "Room"
    column_list = [c.name for c in Rooms.__table__.c]
    column_list += [Rooms.hotel, Rooms.booking]
    icon = "fa-solid fa-bed"
    can_delete = False
