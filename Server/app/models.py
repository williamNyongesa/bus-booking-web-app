from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# User Role Association Table
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"User(email={self.email})"


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Bus(db.Model, SerializerMixin):
    __tablename__ = 'bus'
    id = db.Column(db.Integer, primary_key=True)
    number_of_seats = db.Column(db.Integer, nullable=False)
    cost_per_seat = db.Column(db.Float, nullable=False)
    route = db.Column(db.String(255), nullable=False)
    time_of_travel = db.Column(db.String(50), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schedules = db.relationship('Schedule', backref='bus', lazy=True)

    def __repr__(self):
        return f"Bus(route={self.route}, time_of_travel={self.time_of_travel})"


class Schedule(db.Model, SerializerMixin):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    departure_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))

    def __repr__(self):
        return f"Schedule(departure_time={self.departure_time})"
