import connexion
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_order():
    new_order = Order(user_id=create_order['user_id'],
                      delivery_time=create_order['delivery_time'], priority=create_order['priority'], note=create_order['note'])
    db.session.add(new_order)
    db.session.commit()


connexion_app = connexion.App(__name__, specification_dir="./")
app = connexion_app.app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
connexion_app.add_api("api.yml")


from models import Order

if __name__ == "__main__":
    connexion_app.run(host='0.0.0.0', port=5000, debug=True)