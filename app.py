import os
from threading import Thread
from flask import Flask, request, jsonify, redirect, url_for
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from passlib.hash import pbkdf2_sha256
from flask_oauthlib.provider import OAuth2Provider
from passlib.hash import pbkdf2_sha256

import requests

from api.google_auth import build_service_connection, create_google_oauth_flow, get_authenticated_service, get_user_info
from datetime import datetime
#from data_processing import fetch_data_from_api, process_data
#from models import Actor, Event, Activity
#from influxdb_client import InfluxDBClient

from models import db

 
#from . import db
app = Flask(__name__,static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
db.init_app(app)



#db.init_app(app)

# login_manager = LoginManager(app)
# oauth = OAuth2Provider(app)
global google_credentials
google_credentials = None

# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     tokens = db.relationship('OAuth2Token', backref='user', lazy=True)

# class OAuth2Token(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     token_type = db.Column(db.String(40))
#     access_token = db.Column(db.String(255), unique=True, nullable=False)

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')
    
#     user = User.query.filter_by(username=username).first()
#     if user and pbkdf2_sha256.verify(password, user.password):
#         login_user(user)
#         return jsonify({'message': 'Login successful'}), 200
#     else:
#         return jsonify({'error': 'Invalid credentials'}), 401

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/google/login')
def googleLogin():
    redirect_uri = 'http://localhost:60158/'
    flow = create_google_oauth_flow(redirect_uri)
    google_credentials = flow.run_local_server(port=0)
    authenticated_service = get_authenticated_service(google_credentials)
    user_info = get_user_info(authenticated_service)
    
    print("User's Google ID:", user_info.get('id'))
    print("User's Name:", user_info.get('name'))
    print("User's Email:", user_info.get('email'))

    return "User's Google ID: " + user_info.get('id') + "    User's Name:" + user_info.get('name') + "   User's Email:" + user_info.get('email')
#@app.route('/query/drive/version/reports_v1', methods=['POST'])  
@app.route('/query/<service_name>/version/<version_name>', methods=['POST'])
def query(service_name, version_name):
    redirect_uri = 'http://localhost'
    flow = create_google_oauth_flow(redirect_uri)
    # if google_credentials == None:
    google_credentials = flow.run_local_server(port=0)
    query_service = build_service_connection(service_name, version_name, google_credentials)
    if service_name == 'drive' and version_name == 'reports_v1':
        activities = query_service.activities().list(
            userKey='all',
            applicationName='admin',
            maxResults=10
        ).execute()
        # if 'items' in activities:
        #     for activity in activities['items']:
                
        return activities
    else:
        return 'UNKNOWN SERVICE'
    #Database Initialization and Data Manipulation
from app import app
from models import db, Actor, Event, Activity
from models import db, Actor, Event, Activity

# Create database tables (usually performed once)
with app.app_context():
    db.create_all()

# Create and store objects
 for item in activities:
        actor_data = item.get("actor", {})
        actor = Actor(
            caller_type=actor_data.get("callerType"),
            email=actor_data.get("email"),
            profile_id=actor_data.get("profileId")
        )

        activity_data = item.get("id", {})
        activity = Activity(
            time=datetime.fromisoformat(activity_data.get("time")),
            unique_qualifier=activity_data.get("uniqueQualifier"),
            application_name=activity_data.get("applicationName"),
            customer_id=activity_data.get("customerId"),
            actor=actor,
            ip_address=item.get("ipAddress")
        )

        events_data = item.get("events", [])
        for event_data in events_data:
            event = Event(
                type=event_data.get("type"),
                name=event_data.get("name"),
                activity=activity,
                parameters=json.dumps(event_data.get("parameters"))
            )



    





   #

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     admin_user = User.query.filter_by(username='admin').first()
    #     if(admin_user is None):
    #         admin_user = User(username='admin', password=pbkdf2_sha256.hash("333"))
    #         db.session.add(admin_user)
    #         db.session.commit()
    app.run(debug=True)
