#!/usr/bin/env python
# coding=utf-8
from person import Person
from api import API

if __name__ == '__main__':

    person = Person(name='Gala')
    db_api = API()
    db_api.save(person)
