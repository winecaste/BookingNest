from typing import Any

from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[dict[str, Any]]
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int]

    rooms: Mapped[list["Rooms"]] = relationship(back_populates='hotel')

    def __str__(self):
        return f"Hotel: {self.name}"
