from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash

db = SQLAlchemy()

bcrypt = Bcrypt()
# roles_users = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )

class User(db.Model, UserMixin, SerializerMixin):
    
    __tablename__ = 'users'

    serialize_rules = ("-role.users",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String,nullable=False)
    active = db.Column(db.Boolean(), default=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    # password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"User(email={self.email})"
    @hybrid_property
    def password_hash(self):
        raise AttributeError("password hash cannot be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )
class Bus(db.Model, SerializerMixin):
    __tablename__ = 'bus'

    serialize_rules = ("-users.bus","-schedule.buses",)

    id = db.Column(db.Integer, primary_key=True)
    number_of_seats = db.Column(db.Integer, nullable=False)
    cost_per_seat = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(255), nullable=False)
    time_of_travel = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    schedules = db.relationship('Schedule', backref='bus', lazy=True)

    def __repr__(self):
        return f"Bus(route={self.route}, time_of_travel={self.time_of_travel})"


class Role(db.Model,SerializerMixin):
    __tablename__ = 'roles'

    serialize_rules = ("-users.role",)
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    users = db.relationship('User', backref= 'role')


class Schedule(db.Model, SerializerMixin):
    __tablename__ = 'schedules'

    serialize_rules = ("-bus.schedules")
    id = db.Column(db.Integer, primary_key=True)
    departure_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    price = db.Column(db.Integer)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))


    def __repr__(self):
        return f"Schedule(departure_time={self.departure_time})"
    
    @validates("price")
    def validate_price(self, key, price):
        price = int(price)
        if price < 1 or price > 110:
            raise ValueError("Price must be between 1 and 110")
        
        return price
