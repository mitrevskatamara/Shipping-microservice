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
    name = db.Column(db.String(40), nullable=False)
    location = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.column(db.String)
    courier_assigned = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Boolean, nullable=False)
    order_state = db.Column(db.Enum(OrderState), nullable=False)
    delivery_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


