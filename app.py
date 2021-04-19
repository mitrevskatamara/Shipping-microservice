import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_order():
    new_order = Order(user_id=create_order['user_id'],
                      delivery_time=create_order['delivery_time'],
                      priority=create_order['priority'], note=create_order['note'])
    db.session.add(new_order)
    db.session.commit()
    return {'user_id': Order.user_id}


def add_courier(courier_body):
    new_courier = Courier(id=courier_body['id'], name=courier_body['name'],
                          location=courier_body['location'])
    db.session.add(new_courier)
    db.session.commit()

    return {
        'courier_id': new_courier.id, 'courier_name': new_courier.name,
        'courier_location': new_courier.location}

def find_user_order(user_id):
    order = Order.query.filter_by(user_id=user_id).all()
    if order:
        return {
            'user_id' : order.user_id,
            'order_state' : order.order_state,
            'note' : order.note,
            'delivery_time' : order.delivery_time,
            'courier_assigned' : order.courier_assigned
        }
    else:
        return {'message':'error not found'}, 400

def edit_order(id, createorder_body):
    order = db.session.query(Order).filter_by(id=id).first()
    if not order:
        return {'error': '{} not found'.format(id)}, 404

    order.note = createorder_body['note']
    order.courier_assigned = createorder_body['courier_assigned']
    order.priority = createorder_body['priority']
    order.order_state = createorder_body['order_state']
    order.delivery_time = createorder_body['delivery_time']
    order.user_id = createorder_body['user_id']

    db.session.commit()

    return {'id': order.id,
            'note': order.note,
            'courier_assigned': order.courier_assigned,
            'priority': order.priority,
            'order_state': order.order_state,
            'delivery_time': order.delivery_time,
            'user_id': order.user_id}





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
