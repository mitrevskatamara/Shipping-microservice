from app import db
import enum

class OrderState(enum.Enum):
    Approved = 1
    Accepted = 2
    Preparing = 3
    ReadyForPickUp = 4
    PickedUp = 5
    Delivered = 6


class Courier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    courier_assigned = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Boolean, nullable=False)
    order_state = db.Column(db.Enum(OrderState))
    delivery_time = db.Column(db.String)


