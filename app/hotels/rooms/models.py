from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base
from sqlalchemy import ForeignKey
from typing import Any


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[dict[str, Any]]
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    hotel: Mapped["Hotels"] = relationship( back_populates='rooms')
    booking: Mapped[list["Bookings"]] = relationship(back_populates="room")

    def __str__(self):
        return f"Room: {self.name}"
