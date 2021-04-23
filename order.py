from marshmallow import Schema, fields


class CourierSchema(Schema):
    courierId = fields.Number()
    name = fields.Str()
    location = fields.Str()


schema = CourierSchema()


def result_courier(courier):
    result = dict(courierId=courier.courierId, name=courier.name, location=courier.location)
    return schema.dump(result)


class OrderSchema(Schema):
    orderId = fields.Number()
    description = fields.Str()
    courier_assigned = fields.Number()
    priority = fields.Boolean()
    order_state = fields.Str()
    delivery_time = fields.Str()


schema = OrderSchema()


def result_order(order):
    result = dict(orderId=order.orderId, description=order.description,
                  courier_assigned= order.courier_assigned,
                  priority = order.priority, order_state = order.order_state,
                  delivery_time = order.delivery_time)
    return schema.dump(result)