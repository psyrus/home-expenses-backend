from .base import Base
import string
from random import choice

from sqlalchemy import (Column, Integer, String, Unicode, UnicodeText, DateTime,
                        create_engine)
import random
from datetime import datetime


class Test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))
    init_date = Column(DateTime, nullable=False)
    test_value = Column(String(50))

    def __init__(self, name):
        basic_value = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus ut pulvinar nibh. Fusce sed eros vel nisl pharetra faucibus. Sed est felis, imperdiet vel auctor a, suscipit eget neque. Donec finibus vitae urna eu malesuada. Pellentesque vitae ultrices erat. Integer semper, dolor non faucibus rutrum, turpis mauris feugiat leo, sit amet venenatis libero orci nec velit. Nullam vehicula, metus vitae aliquam pellentesque, nunc sapien bibendum ligula, a gravida diam tortor a erat. Nam ac vehicula tortor, at feugiat sem. In eu libero a sapien imperdiet vehicula at sed massa. Quisque aliquam turpis id augue sagittis interdum. "
        start = random.randint(0, len(basic_value)//2)
        end = random.randint(start, len(basic_value))
        self.name = name
        self.init_date = datetime.now()
        self.test_value = basic_value[start:end]
