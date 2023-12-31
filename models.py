from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, DateTime, String, JSON
from sqlalchemy.ext.declarative import declarative_base


db = SQLAlchemy()
from app import db 
Base = declarative_base()



from sqlalchemy import  ForeignKey
from sqlalchemy.orm import relationship


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    caller_type = Column(String)
    email = Column(String)
    profile_id = Column(String)
    
    # Define the one-to-many relationship with Activity
    activities = relationship('Activity', back_populates='actor')

    def __init__(self, caller_type, email, profile_id):
        self.caller_type = caller_type
        self.email = email
        self.profile_id = profile_id

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    name = Column(String)
    activity_id = Column(Integer, ForeignKey('activities.id'))
    #parameters = Column(JSON)
    
    # Define the one-to-one relationship with Activity
    activity = relationship('Activity', back_populates='event')

    def __init__(self, type, name, parameters=None):
        self.type = type
        self.name = name
        self.parameters = parameters

class Activity(Base):
    __tablename__ = 'activities'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    unique_qualifier = Column(String)
    application_name = Column(String)
    customer_id = Column(String)
    actor_id = Column(Integer, ForeignKey('actors.id'))
    ip_address = Column(String)

    # Define the many-to-one relationship with Actor
    actor = relationship('Actor', back_populates='activities')
    
    # Define the one-to-one relationship with Event
    event = relationship('Event', uselist=False, back_populates='activity')

    def __init__(self, time, unique_qualifier, application_name, customer_id, actor_id, ip_address):
        self.time = time
        self.unique_qualifier = unique_qualifier
        self.application_name = application_name
        self.customer_id = customer_id
        self.actor_id = actor_id
        self.ip_address = ip_address



