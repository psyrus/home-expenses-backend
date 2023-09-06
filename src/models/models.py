# coding: utf-8
from sqlalchemy import (Column, DateTime, Integer, String, ForeignKey, func)
from sqlalchemy.orm import relationship, mapped_column

from .base import Base


class ExpenseAllocation(Base):
    __tablename__ = 'expense_allocation'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    payer_id = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'))
    expense_id = mapped_column(ForeignKey('expenses.id'), ForeignKey('expenses.id'))
    allocation_percent = mapped_column(Integer)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime)
    state_id = mapped_column(ForeignKey('payment_state.id'))

    expense = relationship(
        'Expense', primaryjoin='ExpenseAllocation.expense_id == Expense.id', backref='expense_expense_allocations')
    payer = relationship(
        'User', primaryjoin='ExpenseAllocation.payer_id == User.id', backref='user_expense_allocations')
    state = relationship(
        'PaymentState', primaryjoin='ExpenseAllocation.state_id == PaymentState.id', backref='expense_allocations')


class Expense(Base):
    __tablename__ = 'expenses'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_id = mapped_column(ForeignKey('groups.id'), ForeignKey('groups.id'))
    registered_by_user = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'))
    expense_date = mapped_column(DateTime)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime)

    group = relationship(
        'Group', primaryjoin='Expense.group_id == Group.id', backref='group_expenses')
    user = relationship(
        'User', primaryjoin='Expense.registered_by_user == User.id', backref='user_expenses')


class GroupMember(Base):
    __tablename__ = 'group_members'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at = mapped_column(DateTime, server_default=func.now())
    group_id = mapped_column(ForeignKey('groups.id'), ForeignKey('groups.id'))
    user_id = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'))
    permission_level = mapped_column(ForeignKey('permissions.id'))

    group = relationship(
        'Group', primaryjoin='GroupMember.group_id == Group.id', backref='group_group_members')
    permission = relationship(
        'Permission', primaryjoin='GroupMember.permission_level == Permission.id', backref='group_members')
    user = relationship(
        'User', primaryjoin='GroupMember.user_id == User.id', backref='user_group_members')


class Group(Base):
    __tablename__ = 'groups'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_name = mapped_column(String, unique=True)
    created_by = mapped_column(ForeignKey('users.id'), ForeignKey('users.id'))
    created_at = mapped_column(DateTime, server_default=func.now())

    user = relationship(
        'User', primaryjoin='Group.created_by == User.id', backref='user_groups')

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, group_name={self.group_name!r}, created_by={self.created_by!r}, created_at={self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"

class PaymentState(Base):
    __tablename__ = 'payment_state'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    state_name = mapped_column(String)


class Permission(Base):
    __tablename__ = 'permissions'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at = mapped_column(DateTime, server_default=func.now())
    name = mapped_column(String)
    description = mapped_column(String(50))


class User(Base):
    __tablename__ = 'users'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    auth_provider_id = mapped_column(String, unique=True)
    username = mapped_column(String)
    email = mapped_column(String, unique=True)
    created_at = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, created_at={self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"
