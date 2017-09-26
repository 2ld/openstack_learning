### 前言
OpenStack中的数据库应用主要是关系型数据库，主要使用的是MySQL数据库。当然也有一些NoSQL的应用，比如Ceilometer项目。就SQL数据库本身的应用而言，OpenStack的项目和其他项目并没有什么区别，也是采用ORM技术对数据进行增删改查而已。

主要介绍OpenStack项目中对关系型数据库的应用的基础知识，更多的是涉及ORM库的使用。所设计到的数据库均为MySQL数据库。

### ORM的选择
#### 什么是ORM
ORM的全称是Object-Relational Mapping，即对象关系映射，是一种利用编程语言的对象来表示关系数据库中的数据的技术，其更形式化的定义可以参考Wiki页面[Orject-relational mapping](https://en.wikipedia.org/wiki/Object-relational_mapping)。简单的说，ORM就是把数据库的一张表和编程语言中的一个对象对应起来，这样我们在编程语言中操作一个对象的时候，实际上就是在操作这张表，ORM（一般是一个库）负责把我们对一个对象的操作转换成对数据库的操作。
#### Python中的ORM实现
在Python中也存在多种ORM的实现，最著名的两种是Django的Model层的ORM实现，以及SQLAlchemy库。OpenStack基本上都是Python项目，所以在OpenStack中，ORM主要是使用了SQLAlchemy库（Keystone、Nova、Neutron等）。

### SQLAlchemy
#### SQLAlchemy简介
SQLAlchemy项目是Python中最著名的ORM实现，不仅在Python项目中也得到了广泛的应用，而且对其他语言的ORM有很大的影响。OpenStack一开始选择这个库，也是看中了它足够稳定、足够强大的特点。

#### SQLAlchemy的架构
SQLAlchemy的总体架构图如下：
![](http://vpbvmw.eos.eayun.com/images/sqla_arch_small.png)

SQLAlchemy这个库分为两层：
- 上面这层是ORM层，为用户提供ORM接口，即通过操作Python对象来实现数据库操作的接口。
- 下面这层是Core层，这层包含了Schema/Types、SQL Expression Language、Engine这三个部分：
  - SQL Expression Language是SQLAlchemy中实现的一套SQL表达系统，主要是实现了对SQL的DML(Data Manipulation Language)的封装。这里实现了对数据库的SELECT、DELETE、UPDATE等语句的封装。SQL Expression Language是实现ORM层的基础。
  - Schema/Types这部分主要是实现了对SQL的DDL(Data Definition Language)的封装。实现了Table类用来表示一个表，Column类用来表示一个列，也是实现了将数据库的数据类型映射到Python的数据类型。上面的SQL Expression Language的操作对象就是这里定义的Table。
  - Engine实现了对各种不同的数据库客户端的封装和调度，是所有SQLAlchemy应用程序的入口点，要使用SQLAlchemy库来操作一个数据库，首先就要有一个Engine对象，后续的所有对数据库的操作都要通过这个Engine对象来进行。
- 最后，SQLAlchemy还要依赖各个数据库驱动的DBAPI接口来实现对数据库服务的调用。DBAPI是Python定义的数据库API    的实现规范，具体见[PEP0249](https://www.python.org/dev/peps/pep-0249/)。 

### SQLAlchemy的使用

#### 创建engine
首先需要确定需要连接的数据库信息，然后就可以通过`sqlalchemy`库中的`create_engine`方法创建`engine`,代码如下：
```
from sqlalchemy import create_engine

engine = create_engine('dialect+driver://username:password@host:port/database', echo=True)
```
其中，`dialect`就是指`DBMS`的名称，一般可选的值有：`postgresql`、 `mysql`、`sqlite`等。`driver`就是指驱动的名称，如果不指定，SQLAlchemy会使用默认值。`database`就是指`DBMS`中的一个数据库，一般是指通过`CREATE DATABASE`语句创建的数据库。`echo`为`True`时，控制台会打印原生的SQL，默认为`FALSE`。
`create_engine`函数还支持其它参数，详情请参考官方文档：[Engine Configuration](http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html)。

#### 创建session
**会话**(session)是我们通过SQLAlchemy来操作数据库的入口。一般来说，应用程序的代码是不直接使用Engine对象的，而是把Engine对象交给ORM去使用，或者创建session对象来使用。
要是用session，我们需要先通过sessionmaker函数创建一个session类，然后通过这个类的实例来使用会话，如下所示：
```
from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker(bind=engine)
session = DBSession()
```
我们通过`sessionmaker`的`bind`参数把`Engine`对象传递给`DBSession`去管理。然后，`DBSession`实例化的对象`session`就能被我们使用了。

#### 定义映射类
定义映射类，在SQLAlchemy中，这是通过Declarative的系统来完成的。如果要使用Declarative系统，你需要为所有映射类创建一个基类，这个基类用来维护所有映射类的元信息。如下：
```
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```
假设我们在数据库中有一个表Person，这个表有两个列，分别是id和name，那么我们创建的映射类如下：
```
from sqlalchemy import Column, Integer, String

# 这里的基类Base是上面我们通过declarative_base函数生成的
class Person(Base):
    __tablename__ = 'person'

    id = Column(Interger, primary_key=True)
    name = Column(String(250), nullable=False)
```

### CRUD
通过代码体现如何使用SQlAlchemy实现数据库的基本操作（CRUD），代码格式和规范符合Python的要求。
首先需要定义映射类`Person`:
```
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
```
然后定义`Person`的`API`，主要是针对`person`表的常规操作：
```
#!/usr/bin/env python
# coding=utf-8
from person import Person
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, exc

connect = 'dialect+driver://username:password@host:port/database'

class API(object):
    def __init__(self):
        self.engine = create_engine(connect, echo=True)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def save(self, person):
        self.session.add(person)
        self.session.commit()

    def update(self, person):
        self.session.query(Person).filter_by(id=person.id).\
            update({'name': person.name})
        self.session.commit()

    def delete(self, person_id):
        person = self.query(person_id)
        self.session.delete(person)
        self.session.commit()

    def query_by_id(self, person_id):
        person = None
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
```

其中查询、更新的方法有很多种，详情请参考[SQLAlchemy ORM](http://docs.sqlalchemy.org/en/rel_1_0/orm/index.html)。