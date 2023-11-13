# coding: utf-8
from sqlalchemy import (Boolean, DateTime, Integer, String, ForeignKey, func)
from sqlalchemy.orm import relationship, mapped_column, validates

from .base import Base

class Category(Base):
    __tablename__ = 'categories'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = mapped_column(String, unique=True, nullable=False)

    @validates('id', 'name')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value

class Expense(Base):
    __tablename__ = 'expenses'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    registered_by_user = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'), nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime)

    category = mapped_column(ForeignKey('categories.id'), nullable=False)
    expense_date = mapped_column(DateTime, nullable=False)
    cost = mapped_column(Integer, nullable=False)
    description = mapped_column(String)
    paid_back = mapped_column(Boolean, default=False)

    @validates('id', 'registered_by_user', 'created_at', 'category', 'expense_date', 'cost', 'paid_back')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value

    user_ref = relationship(
        'User', primaryjoin='Expense.registered_by_user == User.id')
    category_ref = relationship(
        'Category', primaryjoin='Expense.category == Category.id')

class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    auth_provider_id = mapped_column(String, unique=True, nullable=False)
    username = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True)
    created_at = mapped_column(DateTime, server_default=func.now())

    @validates('id', 'auth_provider_id', 'username')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, created_at={self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"

class AccessToken(Base):
    __tablename__ = 'accesstokens'

    id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    registered_to_user = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'), nullable=False)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    expires = mapped_column(DateTime, nullable=False)
    token_value = mapped_column(String, nullable=False)

    @validates('id', 'registered_to_user ', 'created_at', 'expires', 'token_value')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value
