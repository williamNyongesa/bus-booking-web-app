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
    
    # Relationships
    buses = db.relationship('Bus', backref='owner', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    license_number = db.Column(db.String(20), unique=True, nullable=False)
    user = db.relationship('User', backref='driver', lazy=True)

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

