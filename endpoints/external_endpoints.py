from functools import wraps
import connexion
import urllib3
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import jwt
import time
from app import db


user_ms_base_url = 'http://localhost:5001/api'
location_ms_url = 'http://localhost:5003/api/locations'



