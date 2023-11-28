from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# roles_users = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )

class User(db.Model, UserMixin, SerializerMixin):
    
    __tablename__ = 'users'

    serialize_rules = ("-role.users",)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return f"User(email={self.email})"
    
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
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))

    def __repr__(self):
        return f"Schedule(departure_time={self.departure_time})"
