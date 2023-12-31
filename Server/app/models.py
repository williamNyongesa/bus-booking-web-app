from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
bcrypt = Bcrypt()

# Association table for the many-to-many relationship
user_schedule = db.Table(
    'user_schedule',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('schedule_id', db.Integer, db.ForeignKey('schedules.id'), primary_key=True)
)


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ("-bookings.users","-user_role.users",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    password = db.Column(db.String)

    # Many-to-many relationship with Schedule through the user_schedule association table
    bookings = db.relationship('Schedule', secondary=user_schedule, back_populates='users')


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @validates("email")
    def validate_email(self, key, email):
        assert "@" in email, "Invalid email address"
        return email
    
    @validates("password")
    def validate_password(self, key, password):
        # At least 8 characters, one uppercase letter, one lowercase letter, and one digit
        assert len(password) >= 8, "Password must be at least 8 characters long"
        assert any(
            char.isupper() for char in password
        ), "Password must contain at least one uppercase letter"
        assert any(
            char.islower() for char in password
        ), "Password must contain at least one lowercase letter"
        assert any(
            char.isdigit() for char in password
        ), "Password must contain at least one digit"
        return password


class Bus(db.Model, SerializerMixin):
    __tablename__ = 'bus'

    serialize_rules = ("-user.buses", "-schedules.bus",)

    id = db.Column(db.Integer, primary_key=True)
    number_of_seats = db.Column(db.Integer, nullable=False)
    cost_per_seat = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(255), nullable=False)
    time_of_travel = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    schedules = db.relationship('Schedule', backref='bus', lazy=True)

    def __repr__(self):
        return f"Bus(route={self.route}, time_of_travel={self.time_of_travel})"

class Schedule(db.Model, SerializerMixin):
    __tablename__ = 'schedules'

    serialize_rules = ("-bus.schedules","-users.bookings",)

    id = db.Column(db.Integer, primary_key=True)
    departure_place = db.Column(db.String(255), nullable=False)
    arrival_place = db.Column(db.String(255), nullable=False)
    departure_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    price = db.Column(db.Integer)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))


    # Many-to-many relationship with User through the user_schedule association table
    users = db.relationship('User', secondary=user_schedule, back_populates='bookings')

    def __repr__(self):
        return f"Schedule(departure_time={self.departure_place}, arrival_place={self.arrival_place}, departure_time={self.departure_time})"
    
    @validates("price")
    def validate_price(self, key, price):
        price = int(price)
        if price < 1 or price > 5000:
            raise ValueError("Price must be between 1 and 5000")
        
        return price
