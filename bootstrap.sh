#!/bin/sh
export FLASK_APP=./app.py
pipenv install
pip install influxdb

pipenv run flask --debug run -h 0.0.0.0