import uuid

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )

    balance: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default='0'
    )
