from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app.models.base import BaseModel

Base = declarative_base()

class DatabaseController(Base, BaseModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def create(cls, session, **kwargs):
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def read(cls, session, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def update(cls, session, id, **kwargs):
        instance = session.query(cls).filter_by(id=id).first()
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.commit()
            return instance
        return None

    @classmethod
    def delete(cls, session, id):
        instance = session.query(cls).filter_by(id=id).first()
        if instance:
            session.delete(instance)
            session.commit()
            return True
        return False

    @classmethod
    def all(cls, session):
        return session.query(cls).all()
