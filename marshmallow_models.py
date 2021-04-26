from marshmallow import Schema, fields


class CourierSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    location = fields.Str()


schemaCourier = CourierSchema()


def result_courier(courier):
    result = dict(id=courier.id, name=courier.name, location=courier.location)
    return schemaCourier.dump(result)


class OrderSchema(Schema):
    id = fields.Number()
    description = fields.Str()
    courier_assigned = fields.Number()
    priority = fields.Boolean()
    order_state = fields.Str()
    delivery_time = fields.Str()


schemaOrder = OrderSchema()


def result_order(order):
    result = dict(id=order.id, description=order.description,
                  courier_assigned= order.courier_assigned,
                  priority = order.priority, order_state = order.order_state,
                  delivery_time = order.delivery_time)
    return schemaOrder.dump(result)
