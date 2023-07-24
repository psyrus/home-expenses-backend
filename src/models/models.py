# coding: utf-8
from sqlalchemy import (Column, DateTime, Integer, String, ForeignKey, func)
from sqlalchemy.orm import relationship

from .base import Base


class ExpenseAllocation(Base):
    __tablename__ = 'expense_allocation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    payer_id = Column(ForeignKey('users.id'), ForeignKey('users.id'))
    expense_id = Column(ForeignKey('expenses.id'), ForeignKey('expenses.id'))
    allocation_percent = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    state_id = Column(ForeignKey('payment_state.id'))

    expense = relationship(
        'Expense', primaryjoin='ExpenseAllocation.expense_id == Expense.id', backref='expense_expense_allocations')
    payer = relationship(
        'User', primaryjoin='ExpenseAllocation.payer_id == User.id', backref='user_expense_allocations')
    state = relationship(
        'PaymentState', primaryjoin='ExpenseAllocation.state_id == PaymentState.id', backref='expense_allocations')


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(ForeignKey('groups.id'), ForeignKey('groups.id'))
    registered_by_user = Column(ForeignKey('users.id'), ForeignKey('users.id'))
    expense_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    group = relationship(
        'Group', primaryjoin='Expense.group_id == Group.id', backref='group_expenses')
    user = relationship(
        'User', primaryjoin='Expense.registered_by_user == User.id', backref='user_expenses')


class GroupMember(Base):
    __tablename__ = 'group_members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    group_id = Column(ForeignKey('groups.id'), ForeignKey('groups.id'))
    user_id = Column(ForeignKey('users.id'), ForeignKey('users.id'))
    permission_level = Column(ForeignKey('permissions.id'))

    group = relationship(
        'Group', primaryjoin='GroupMember.group_id == Group.id', backref='group_group_members')
    permission = relationship(
        'Permission', primaryjoin='GroupMember.permission_level == Permission.id', backref='group_members')
    user = relationship(
        'User', primaryjoin='GroupMember.user_id == User.id', backref='user_group_members')


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_by = Column(ForeignKey('users.id'), ForeignKey('users.id'))
    created_at = Column(DateTime)

    user = relationship(
        'User', primaryjoin='Group.created_by == User.id', backref='user_groups')


class PaymentState(Base):
    __tablename__ = 'payment_state'

    id = Column(Integer, primary_key=True, autoincrement=True)
    state_name = Column(String)


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime)
    name = Column(String)
    description = Column(String(50))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, created_at={self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"
