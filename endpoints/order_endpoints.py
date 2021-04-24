from utilities import has_role
from models import Order, OrderState
from app import db
from order import *


def create_order(createorder_body):
    new_order = Order(id=createorder_body['id'], description=createorder_body['description'],
                      courier_assigned=createorder_body['courier_assigned'],
                      priority=createorder_body['priority'],
                      order_state=createorder_body['order_state'],
                      delivery_time=createorder_body['delivery_time'],
                      )
    db.session.add(new_order)
    db.session.commit()
    return result_order(new_order)


def find_user_order(user_id):
    order = Order.query.filter_by(user_id=user_id).all()
    if order:
        return result_order(order)
    else:
        return {'message':'error not found'}, 400


def edit_order(id, createorder_body):
    order = db.session.query(Order).filter_by(id=id).first()
    if not order:
        return {'error': '{} not found'.format(id)}, 404

    order.description = createorder_body['description']
    order.courier_assigned = createorder_body['courier_assigned']
    order.priority = createorder_body['priority']
    order.order_state = createorder_body['order_state']
    order.delivery_time = createorder_body['delivery_time']

    db.session.commit()

    return result_order(order)


def updateOrderState(id, state):
    order = db.session.query(Order).filter_by(id=id).first()

    if not order:
        return {'error': '{} not found'.format(id)}, 404

    order.order_state = state
    db.session.commit()
    return result_order(order)


order_schema = CourierSchema()


def list_orders():
    orders = db.session.query(Order).all()
    if not orders:
        return {'message':'error not found'}, 404

    for order in orders:
        return order_schema.dump(order)


def delete_order(id):
    order = db.session.query(Order).filter_by(id=id).first()

    if order:
        db.session.delete(order)
        db.session.commit()

        return {f'The order with {id} id is deleted!'}, 200
    else:
        return {'message':'error not found'}, 404