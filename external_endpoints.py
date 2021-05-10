import requests
import json

location_ms_url = 'http://localhost:5001/api/locations'
user_ms_url = 'http://localhost:5002/api'
payments_ms_url = 'http://localhost:5004/api'


# USER MICROSERVICE
def get_all_users_details():
    response = requests.get(user_ms_url + 'user/all')
    if response.status_code == 200:
        users_list = json.dumps(response.json())
        return users_list
    else:
        return False


def get_user_details(user_id):
    response = requests.get(user_ms_url + 'user/details/' + user_id)
    if response.status_code == 200:
        user = json.dumps(response.json())
        return user
    else:
        return False


# LOCATIONS MICROSERVICE
def get_all_bicycle_stores():
    response = requests.get(location_ms_url + '/bicycle_stores/all')
    if response.status_code == 200:
        stores = json.dumps(response.json())
        return stores
    else:
        return False


def get_single_bicycle_store(store_id):
    response = requests.get(location_ms_url + '/bicycle_stores/' + store_id)
    if response.status_code == 200:
        singlestore = json.dumps(response.json())
        return singlestore
    else:
        return False


# PAYMENTS MICROSERVICE
def transaction_details(id):
    response = requests.get(payments_ms_url + '/transactions/' + id)
    if response.status_code == 200:
        return True
    else:
        return False