import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import jwt
from functools import wraps
from flask import request, abort
from marshmallow_models import *

from consul_functions import get_host_name_IP, get_consul_service, register_to_consul


JWT_SECRET = 'MY JWT SECRET'

# consul_port = 8500
# service_name = "shipping"
# service_port = 5000


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


### JWT

def validate_request(request_body):
    invalid_parameters = []

    for key in request_body.keys():
        value = request_body[key]

        if value is None:
            invalid_parameters.append(key)
        else:
            if ((type(value) is str) and not (value.strip())) or ((type(value) is int) and (value <= 0)):
                invalid_parameters.append(key)

    return tuple(invalid_parameters)


def has_role(arg):
    def has_role_inner(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            try:
                headers = request.headers
                if 'AUTHORIZATION' in headers:
                    token = headers['AUTHORIZATION'].split(' ')[1]
                    decoded_token = decode_token(token)
                    for role in arg:
                        if role in decoded_token['roles']:
                            return fn(*args, **kwargs)
                    abort(401)
                return fn(*args, **kwargs)
            except Exception as e:
                abort(401)

        return decorated_view

    return has_role_inner


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])



### COURIER ENDPOINTS

courier_schema = CourierSchema()

@has_role('shipping_admin')
def add_courier(courier_body):
    new_courier = models.Courier(id=courier_body['id'],
                          name=courier_body['name'],
                          location=courier_body['location'])
    db.session.add(new_courier)
    db.session.commit()
    return result_courier(new_courier)


@has_role(['shipping_admin', 'shipping_courier'])
def edit_courier(id, courier_body):
    courier = db.session.query(models.Courier).filter_by(id=id).first()

    if not courier:
        return {'error': f'Courier {id} not found'}, 404

    courier.name = courier_body['name']
    courier.location = courier_body['location']
    db.session.commit()

    return result_courier(courier)


schema = CourierSchema()


@has_role('shipping_admin')
def list_couriers():
    couriers = db.session.query(models.Courier).all()
    if not couriers:
        return {'message': 'No couriers found!'}, 404

    return schema.dump(couriers, many=True)


@has_role('shipping_admin')
def delete_courier(id):
    courier = db.session.query(models.Courier).filter_by(id=id).first()

    if courier:
        db.session.delete(courier)
        db.session.commit()
    else:
        return {'error': 'Not found'}, 404

    return {'message': 'Successfully'}, 200


### ORDER ENDPOINTS

orderschema = OrderSchema()


@has_role(['shipping_user', 'shopping_cart'])
def create_order(create_order_body):
    new_order = models.Order(id=create_order_body['id'],
                      userId=create_order_body['userId'],
                      description=create_order_body['description'],
                      courier_assigned=create_order_body['courier_assigned'],
                      priority=create_order_body['priority'],
                      order_state=create_order_body['order_state'],
                      delivery_time=create_order_body['delivery_time'])

    db.session.add(new_order)
    db.session.commit()
    return result_order(new_order)


@has_role(['shipping_admin', 'shipping_user', "shipping_courier"])
def find_user_order(user_id):
    order = models.Order.query.filter_by(user_id=user_id).all()
    if order:
        return result_order(order)
    else:
        return {'error': f'User {id} not found'}, 400


@has_role(['shipping_user'])
def edit_order(id, createorder_body):
    order = db.session.query(models.Order).filter_by(id=id).first()
    if not order:
        return {'error': f'Order {id} not found'}, 404

    order.description = createorder_body['description']
    order.courier_assigned = createorder_body['courier_assigned']
    order.priority = createorder_body['priority']
    order.order_state = createorder_body['order_state']
    order.delivery_time = createorder_body['delivery_time']

    db.session.commit()

    return result_order(order)


@has_role(['shipping_admin', 'shipping_courier'])
def updateorderstate(id, state):
    order = db.session.query(models.Order).filter_by(id=id).first()

    if not order:
        return {'error': f'Order {id} not found!'}, 404

    order.order_state = state
    db.session.commit()
    return result_order(order)


@has_role(['shipping_admin', 'shipping_courier'])
def list_orders():
    orders = db.session.query(models.Order).all()
    if not orders:
        return {'error':'No orders found!'}, 404

    return orderschema.dump(orders, many=True)


@has_role(['shipping_admin'])
def delete_order(id):
    order = db.session.query(models.Order).filter_by(id=id).first()

    if order:
        db.session.delete(order)
        db.session.commit()
    else:
        return {'error': 'Not found!'}, 404

    return {'message': 'Successfully deleted!'}, 200


connexion_app.add_api("api.yml")

register_to_consul()

import models


if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)

