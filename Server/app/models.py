from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates



db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    #Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True )
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)
    role = db.Column(db.String)


#Possible Suggested relationships
    # buses = db.relationship('Bus', backref='driver')
    # bookings = db.relationship('Booking', backref='user')

    # do we want users to see schedules?


    # validation
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

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    license_number = db.Column(db.String(20), unique=True, nullable=False)
    buses = db.relationship('Bus', backref='driver', lazy=True)
    

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_seats = db.Column(db.Integer, nullable=False)
    cost_per_seat = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(100), nullable=False)
    time_of_travel = db.Column(db.String(20), nullable=False)

    # Foreign Key relationships
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    bookings = db.relationship('Booking', backref='bus', lazy=True)
class Schedule(db.Model, SerializerMixin):
    __tablename__ = 'schedules'


    id = db.Column(db.Integer, primary_key=True)
    departure_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    route = db.Column(db.String, nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'), nullable=False)

    bus = db.relationship('Bus', backref='schedules')
    bookings = db.relationship('Booking', backref='schedule')

    class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Foreign Key relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id', ondelete='CASCADE'), nullable=False)