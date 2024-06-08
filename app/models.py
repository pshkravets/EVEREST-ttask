from flask_login import UserMixin
from flask_migrate import Migrate
from make_celery import flask_app, admin, Controler
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(flask_app)
migrate = Migrate(flask_app, db)


class Gods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    color = db.Column(db.String(50))
    weight = db.Column(db.Float(2))
    price = db.Column(db.Float(2))
    photo = db.Column(db.String(200))
    orders = db.relationship('Order', backref='gods')


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    cities = db.relationship('City', backref='country')


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    addresses = db.relationship('Address', backref='city')


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    addresses = db.relationship('Order', backref='address')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    status = db.Column(db.String(50))
    good_id = db.Column(db.Integer, db.ForeignKey('gods.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(1000), nullable=False)


admin.add_view(Controler(User, db.session))
admin.add_view(Controler(Gods, db.session))
admin.add_view(Controler(Country, db.session))
admin.add_view(Controler(City, db.session))
admin.add_view(Controler(Address, db.session))
admin.add_view(Controler(Order, db.session))



