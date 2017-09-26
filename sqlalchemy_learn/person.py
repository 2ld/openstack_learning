#!/usr/bin/env python
# coding=utf-8
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime

Base = declarative_base()


class TimestampMixin(object):
    create_at = Column(DateTime, default=datetime.now())


class Person(Base, TimestampMixin):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def __repr__(self):
        return "<Person(id='%s', name='%s')>" % (
            self.id, self.name)


if __name__ == '__main__':
    engine = create_engine(
            'mysql://nova:2c66a6cf3e@10.0.0.3/nova_api',
        echo=True)

    Base.metadata.create_all(engine)
