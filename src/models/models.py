# coding: utf-8
from sqlalchemy import (Boolean, Column, DateTime, Integer, String, ForeignKey, func)
from sqlalchemy.orm import relationship, mapped_column, validates, Mapped
from typing import List

from .base import Base

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[String] = mapped_column(String, unique=True, nullable=False)

    @validates('id', 'name')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value

class Expense(Base):
    __tablename__ = 'expenses'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    registered_by_user: Mapped[Integer] = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime)

    category: Mapped[Integer] = mapped_column(ForeignKey('categories.id'), nullable=False)
    expense_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    cost: Mapped[Integer] = mapped_column(Integer, nullable=False)
    description = mapped_column(String)
    paid_back: Mapped[Boolean] = mapped_column(Boolean, default=False)

    @validates('id', 'registered_by_user', 'created_at', 'category', 'expense_date', 'cost', 'paid_back')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value

    user = relationship(
        'User', primaryjoin='Expense.registered_by_user == User.id', backref='user_expenses')
    category_ref = relationship(
        'Category', primaryjoin='Expense.category == Category.id')

class User(Base):
    __tablename__ = 'users'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    auth_provider_id: Mapped[String] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[String] = mapped_column(String, nullable=False)
    email: Mapped[String] = mapped_column(String, unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    @validates('id', 'auth_provider_id', 'username')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, created_at={self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"

class AccessToken(Base):
    __tablename__ = 'accesstokens'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    registered_to_user: Mapped[Integer] = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    expires: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    token_value: Mapped[String] = mapped_column(String, nullable=False)

    @validates('id', 'registered_to_user ', 'created_at', 'expires', 'token_value')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value

class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[String] = mapped_column(String, nullable=False)
    description: Mapped[String] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    members: Mapped[List["GroupMember"]] = relationship(back_populates="group", cascade='all, delete')

    @validates('id', 'name ', 'description', 'created_at', 'members')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value

class GroupMember(Base):
    __tablename__ = 'groupmembers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), ForeignKey('groups.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'), nullable=False)
    is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    group: Mapped["Group"] = relationship(back_populates="members")

    @validates('id', 'group ', 'user', 'is_admin', 'created_at', 'group')
    def empty_string_to_null(self, key, value):
        return None if value == '' else value
