import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class transaction_status(enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    email : Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name : Mapped[str] = mapped_column(String, nullable=False)
    last_name : Mapped[str] = mapped_column(String, nullable = True)
    created_at : Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    wallet : Mapped["Wallet"] = relationship(back_populates="user")

class Wallet(Base):
    __tablename__ = 'wallets'

    id : Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))
    balance : Mapped[float] = mapped_column(Numeric(precision=10, scale=2), CheckConstraint("balance>=0"))
    currency : Mapped[str] = mapped_column(String(3), default='INR')
    created_at : Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    user : Mapped["User"] = relationship(back_populates="wallet")
    incoming_transactions : Mapped[list["Transaction"]] = relationship(
        foreign_keys="[Transaction.to_wallet_id]", back_populates="to_wallet"
    )
    outgoing_transactions : Mapped[list["Transaction"]] = relationship(
        foreign_keys="[Transaction.from_wallet_id]", back_populates="from_wallet"
    )

class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    from_wallet_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("wallets.id"))
    to_wallet_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("wallets.id"))
    amount : Mapped[float] = mapped_column(Numeric(precision=10, scale=2), CheckConstraint("amount>0"))
    status : Mapped[transaction_status] = mapped_column(Enum(transaction_status), default=transaction_status.PENDING)
    created_at : Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    to_wallet : Mapped["Wallet"] = relationship(
        foreign_keys=[to_wallet_id], back_populates="incoming_transactions"
    )
    from_wallet : Mapped["Wallet"] = relationship(
        foreign_keys=[from_wallet_id], back_populates="outgoing_transactions"
    )