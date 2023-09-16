# coding: utf-8
from sqlalchemy import (Column, DateTime, Integer, String, ForeignKey, func)
from sqlalchemy.orm import relationship, mapped_column

from .base import Base


class Expense(Base):
    __tablename__ = 'expenses'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    registered_by_user = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'))
    expense_date = mapped_column(DateTime)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime)

    user = relationship(
        'User', primaryjoin='Expense.registered_by_user == User.id', backref='user_expenses')


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    auth_provider_id = mapped_column(String, unique=True)
    username = mapped_column(String)
    email = mapped_column(String, unique=True)
    created_at = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, created_at={self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"
