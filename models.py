from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Orders(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    product_id = db.Column(db.Integer)

    order_status = db.Column(db.String(100))

    current_location = db.Column(db.String(200))

    delivery_partner = db.Column(db.String(100))

    order_date = db.Column(db.DateTime)


class OrderTracking(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer)

    status = db.Column(db.String(100))

    location = db.Column(db.String(200))

    timestamp = db.Column(db.DateTime)