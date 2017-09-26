#!/usr/bin/env python
# coding=utf-8
from person import Person
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, exc

connect = 'mysql://nova:2c66a6cf3e@10.0.0.3/nova_api'


class API(object):
    def __init__(self):
        self.engine = create_engine(
            'mysql://nova:2c66a6cf3e@10.0.0.3/nova_api',
            echo=True)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def save(self, person):
        self.session.add(person)
        self.session.commit()

    def update(self, person):
        #        conn = self.engine.connect()
        #        stmt = Person.update().values(Person.name = 'haha').where(Person.id == person.id)
        #        conn.execute(stmt)
        self.session.query(Person).filter_by(id=person.id).\
            update({'name': person.name})
        self.session.commit()

    def delete(self, person_id):
        person = self.query(person_id)
        self.session.delete(person)
        self.session.commit()

    def query_by_id(self, person_id):
        person = None
#       query = self.session.query(Person).filter_by(id=person_id)
        text_ = 'select * from person where id = :id'
        query = self.session.query(Person).from_statement(text(text_))\
            .params(id=person_id)
        try:
            person = query.one()
        except exc.NoResultFound:
            # TODO
            pass
        return person

    def query_by_name(self, person_name):
        person = None
        query = self.session.query(Person).\
            filter(Person.name.like('%' + person_name + '%'))
        person = query.all()
        return person

    def query_all(self):
        persons = self.session.query(Person).all()
        return persons

    def create_table(self):
        from sqlalchemy.ext.declarative import declarative_base
        Base = declarative_base()
        Base.metadata.create_all(self.engine)


if __name__ == '__main__':
    db_api = API()
    person_name = 'MamB'
    print db_api.query_by_name(person_name)
