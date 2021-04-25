from utilities import has_role
from models import Courier
from app import db
from order import *

courier_schema = CourierSchema()

@has_role('shipping_admin')
def add_courier(courier_body):
    new_courier = Courier(id=courier_body['id'], name=courier_body['name'],
                          location=courier_body['location'])
    db.session.add(new_courier)
    db.session.commit()
    return result_courier(new_courier)

@has_role(['shipping_admin','shipping_courier'])
def edit_courier(id, courier_body):
    courier = db.session.query(Courier).filter_by(id=id).first()

    if not courier:
        return {'error': '{} not found'.format(id)}, 404

    courier.name = courier_body['name']
    courier.location = courier_body['location']
    db.session.commit()

    return result_courier(courier)

@has_role('shipping_admin')
def list_couriers():
    couriers = db.session.query(Courier).all()
    if not couriers:
        return {'message':'error not found'}, 404

    for courier in couriers:
        return courier_schema.dump(courier)

@has_role('shipping_admin')
def delete_courier(id):
    courier = db.session.query(Courier).filter_by(id=id).first()

    if courier:
        db.session.delete(courier)
        db.session.commit()

        return {f'The courier with {id} id is deleted!'}, 200
    else:
        return {'message':'error not found'}, 404


