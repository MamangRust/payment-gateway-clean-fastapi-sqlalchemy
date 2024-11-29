from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Text, Sequence, TIMESTAMP, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

Base = declarative_base()



# User Model
class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    firstname: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    noc_transfer: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, default="0")
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    topups = relationship('Topup', back_populates='user')
    saldo = relationship('Saldo', back_populates='user')
    transfers_from = relationship('Transfer', foreign_keys='Transfer.transfer_from', back_populates='user_from')
    transfers_to = relationship('Transfer', foreign_keys='Transfer.transfer_to', back_populates='user_to')
    withdraws = relationship('Withdraw', back_populates='user')

    def as_dict(self):
        # Exclude 'password' from the dictionary
        return {k: v for k, v in self.__dict__.items() if k != '_sa_instance_state' and k != 'password'}

# Topup Model
class Topup(Base):
    __tablename__ = 'topups'

    topup_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    topup_no: Mapped[str] = mapped_column(Text, nullable=False)
    topup_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    topup_method: Mapped[str] = mapped_column(Text, nullable=False)
    topup_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship('User', back_populates='topups')

# Saldo Model
class Saldo(Base):
    __tablename__ = 'saldo'

    saldo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    total_balance: Mapped[int] = mapped_column(Integer, nullable=False)
    withdraw_amount: Mapped[int] = mapped_column(Integer, default=0)
    withdraw_time: Mapped[str] = mapped_column(TIMESTAMP)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship('User', back_populates='saldo')

# Transfer Model
class Transfer(Base):
    __tablename__ = 'transfers'

    transfer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transfer_from: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    transfer_to: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    transfer_amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    transfer_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user_from = relationship('User', foreign_keys=[transfer_from], back_populates='transfers_from')
    user_to = relationship('User', foreign_keys=[transfer_to], back_populates='transfers_to')

# Withdraw Model
class Withdraw(Base):
    __tablename__ = 'withdraws'

    withdraw_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    withdraw_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    withdraw_time: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship('User', back_populates='withdraws')