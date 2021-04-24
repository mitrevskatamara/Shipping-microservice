from utilities import has_role
from models import Courier
from app import db
from order import *

courier_schema = CourierSchema()


def add_courier(courier_body):
    new_courier = Courier(id=courier_body['id'], name=courier_body['name'],
                          location=courier_body['location'])
    db.session.add(new_courier)
    db.session.commit()
    return result_courier(new_courier)


def edit_courier(id, courier_body):

    courier = db.session.query(Courier).filter_by(id=id).first()

    if not courier:
        return {'error': '{} not found'.format(id)}, 404

    courier.name = courier_body['name']
    courier.location = courier_body['location']

    db.session.commit()

    return result_courier(courier)


def list_couriers():
    response = {'message': None, 'bicycle_stores': None}
    couriers = db.session.query(Courier).all()

    response['message'] = "Couriers were successfully found"
    response['bicycle_stores'] = [courier_schema.dump(courier) for courier in couriers]
