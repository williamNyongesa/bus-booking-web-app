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