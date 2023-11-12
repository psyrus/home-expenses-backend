from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    
    def get_dict(self):
        from sqlalchemy import inspect
        mapper = inspect(self)
        dict_ = {}
        for column in mapper.attrs:
            key = column.key
            value_type = type(column.loaded_value)
            value = column.loaded_value if not issubclass(value_type, Base) else column.loaded_value.get_dict()
            dict_[key] = value

        return dict_
