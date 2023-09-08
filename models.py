from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, DateTime, String, JSON
from sqlalchemy.ext.declarative import declarative_base


db = SQLAlchemy()
from app import db 
Base = declarative_base()



from sqlalchemy import  ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    caller_type = Column(String)
    email = Column(String)
    profile_id = Column(String)

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    parameters = Column(JSON)

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    unique_qualifier = Column(String)
    application_name = Column(String)
    customer_id = Column(String)
    actor_id = Column(Integer, ForeignKey('actors.id'))
    ip_address = Column(String)

    actor = relationship('Actor', back_populates='activities')
    events = relationship('Event', back_populates='activity')


