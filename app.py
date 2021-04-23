import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from order import *


def create_order(createorder_body):
    new_order = Order(orderId=createorder_body['orderId'],description=createorder_body['description'],
                      courier_assigned = createorder_body['courier_assigned'],
                      priority=createorder_body['priority'],
                      order_state=createorder_body['order_state'],
                      delivery_time=createorder_body['delivery_time'],
                      )
    db.session.add(new_order)
    db.session.commit()
    return result_order(new_order)


def add_courier(courier_body):
    new_courier = Courier(courierId=courier_body['courierId'], name=courier_body['name'],
                          location=courier_body['location'])
    db.session.add(new_courier)
    db.session.commit()
    return result_courier(new_courier)


def find_user_order(user_id):
    order = Order.query.filter_by(user_id=user_id).all()
    if order:
        return result_order(order)
    else:
        return {'message':'error not found'}, 400


def edit_order(orderId, createorder_body):
    order = db.session.query(Order).filter_by(orderId=orderId).first()
    if not order:
        return {'error': '{} not found'.format(orderId)}, 404

    order.note = createorder_body['note']
    order.courier_assigned = createorder_body['courier_assigned']
    order.priority = createorder_body['priority']
    order.order_state = createorder_body['order_state']
    order.delivery_time = createorder_body['delivery_time']
    order.user_id = createorder_body['user_id']

    db.session.commit()

    return result_order(order)


def edit_courier(courierId, courier_body):

    courier = db.session.query(Courier).filter_by(courierId=courierId).first()

    if not courier:
        return {'error': '{} not found'.format(id)}, 404

    courier.name = courier_body['name']
    courier.location = courier_body['location']

    db.session.commit()

    return result_courier(courier)


def updateOrderState(id, state):
    order = db.session.query(Order).filter_by(id=id).first()

    if not order:
        return {'error': '{} not found'.format(id)}, 404

    order.order_state = state
    db.session.commit()
    return result_order(order)


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")

from models import Order, Courier

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)
