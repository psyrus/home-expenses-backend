from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import LoaderCallableStatus
from sqlalchemy.orm.collections import InstrumentedList
class Base(DeclarativeBase):
    
    def get_dict(self):
        from sqlalchemy import inspect
        mapper = inspect(self)
        dict_ = {}
        for column in mapper.attrs:
            key = column.key
            value_type = type(column.loaded_value)
            if value_type is LoaderCallableStatus:
                continue
            if issubclass(value_type, Base):
                value = column.loaded_value.get_dict()
            elif isinstance(column.loaded_value, InstrumentedList):
                value = [i.get_dict() for i in column.loaded_value]
            else:
                value = column.loaded_value
            dict_[key] = value

        return dict_
