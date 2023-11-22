from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property



db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):

    serialize_rules = ("-bookings.user",)
    __tablename__ = 'users'

    #Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True )
    email = db.Column(db.String, unique=True)
    # password = db.Column(db.String, unique=True)
    role = db.Column(db.String)
    _password_hash = db.Column(db.String)

    # one user many bookings
    bookings = db.relationship("Booking", backref = "user")

    def __repr__(self):
        return f"name: {self.username}"
    
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

class Driver(db.Model, SerializerMixin):
    __tablename__ = 'drivers'

    serialize_rules = ("-buses.driver",)
    id = db.Column(db.Integer, primary_key=True)
    
    license_number = db.Column(db.String(20), unique=True, nullable=False)
#   one driver many buses
    buses = db.relationship("Bus", backref = "driver")

class Bus(db.Model, SerializerMixin):
    __tablename__ = "buses"
    serialize_rules = ("-bookings.bus","-driver.buses","-schedules.bus",)
    
    id = db.Column(db.Integer, primary_key=True)
    number_of_seats = db.Column(db.Integer, nullable=False)
    cost_per_seat = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(100), nullable=False)
    time_of_travel = db.Column(db.String(20), nullable=False)

    # one bus many bookings
    bookings = db.relationship("Booking",backref = "bus")
    # many buses one driver
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"))
    #  one bus many schedules
    schedules = db.relationship("Schedule", backref = "bus")

class Schedule(db.Model, SerializerMixin):
    __tablename__ = 'schedules'
    serialize_rules = ("-buses.schedule",)

    id = db.Column(db.Integer, primary_key=True)
    departure_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    route = db.Column(db.String, nullable=False)

    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id'))

class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'
    serialize_rules = ("-users.booking","buses.booking",)
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())



    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.id', ondelete='CASCADE'))