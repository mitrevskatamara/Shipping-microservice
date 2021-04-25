from functools import wraps
import connexion
import urllib3
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import jwt
import time
from app import db
import requests
import json

user_ms_url = 'http://localhost:5002/api'
location_ms_url = 'http://localhost:5001/api/locations'


# USER MICROSERVICE
def get_all_users_details():
    resp = requests.get(user_ms_url + 'user/all')
    if resp.status_code == 200:
        users_list = json.dumps(resp.json())
        return users_list
    else:
        return False


def get_user_details(user_id):
    resp = requests.get(user_ms_url + 'user/details/' + user_id)
    if resp.status_code == 200:
        user = json.dumps(resp.json())
        return user
    else:
        return False


# LOCATIONS MICROSERVICE
def get_all_bicycle_stores():
    resp = requests.get(location_ms_url + '/bicycle_stores/all')
    if resp.status_code == 200:
        stores = json.dumps(resp.json())
        return stores
    else:
        return False


def get_single_bicycle_store(store_id):
    resp = requests.get(location_ms_url + '/bicycle_stores/' + store_id)
    if resp.status_code == 200:
        singlestore = json.dumps(resp.json())
        return singlestore
    else:
        return False


