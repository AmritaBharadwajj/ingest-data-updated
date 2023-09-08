from app import app
from models import db, Actor, Event, Activity
from datetime import datetime

# Create database tables (usually performed once)
with app.app_context():
    db.create_all()

# Create and store objects
actor = Actor(caller_type='user', email='user@example.com', profile_id='123')
db.session.add(actor)

event = Event(type='some_event_type', name='Event Name', activity_id=1, parameters={'key': 'value'})
db.session.add(event)

activity = Activity(time=datetime.now(), unique_qualifier='unique', application_name='My App', customer_id='456', actor_id=1, ip_address='127.0.0.1')
db.session.add(activity)

db.session.commit()
