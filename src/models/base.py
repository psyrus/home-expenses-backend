from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    
    def get_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
