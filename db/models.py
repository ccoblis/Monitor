from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db import utils


Base = declarative_base()


class Info(Base):
    __tablename__ = 'info'

    id = Column(Integer, primary_key=True)
    data = Column(String)

    def save(self):
        session = utils.get_new_session()
        with session.begin():
            session.add(self)

    def _to_dict(self):
        _dict = {col.name: getattr(self, col.name)
        for col in self.__table__.columns}
        return _dict

    def __str__(self):
        return 'User: Name: %s' % self.data

    def __repr__(self):
        return str(self)
