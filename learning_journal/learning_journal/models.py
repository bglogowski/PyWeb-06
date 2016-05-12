
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime,
    desc,
    )

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Unicode(length=255), nullable=False, unique=True)
    body = Column(UnicodeText())
    created = Column(DateTime(timezone=True), default=func.now())
    edited = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).order_by(desc(cls.created)).all()

    @classmethod
    def by_id(cls, id, session=None):
        id = int(id)
        if session is None:
            session = DBSession
        return session.query(cls).get(id)
    

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Unicode(length=255), unique=True, nullable=False)
    password = Column(Unicode(), nullable=True)

    def verify_password(self, password):
        manager = Manager()
        return manager.check(self.password, password)

    @classmethod
    def by_name(cls, username, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).get(username)


Index('my_index', Entry.title, unique=True, mysql_length=255)
