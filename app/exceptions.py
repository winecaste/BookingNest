from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User already exists'


class IncorrectAccessException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect email or password'


class TokenNotExistException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token not exist'


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token expired'


class InvalidTokenException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid token'


class UserIsNotPresent(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'All rooms are booked'


class DateFromCannotBeAfterDateTo(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Date cannot be later than date from'


class DaysHasBeenExceeded(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'The length of stay must be less than 30 days'



