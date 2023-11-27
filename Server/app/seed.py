from faker import Faker
from app import db
from models import User, Role, Bus, Schedule
from random import choice, randint

fake = Faker()

def delete_data():
    db.session.query(User).delete()
    db.session.query(Role).delete()
    db.session.query(Bus).delete()
    db.session.query(Schedule).delete()
    db.session.commit()

def seed_roles():
    roles = ['admin', 'driver', 'customer']
    for role_name in roles:
        role = Role(name=role_name)
        db.session.add(role)
    db.session.commit()

def seed_users():
    for _ in range(10):
        user = User(email=fake.email(), password="password")
        db.session.add(user)
    db.session.commit()

def seed_buses():
    drivers = User.query.filter_by(roles=[Role.query.filter_by(name='driver').first()]).all()
    
    for _ in range(10):
        bus = Bus(
            number_of_seats=randint(20, 60),
            cost_per_seat=fake.random_int(min=10, max=50),
            route=fake.word(),
            time_of_travel=fake.time(),
            driver_id=choice(drivers).id
        )
        db.session.add(bus)
    db.session.commit()

def seed_schedules():
    buses = Bus.query.all()

    for _ in range(10):
        schedule = Schedule(
            departure_time=fake.date_time_this_year(),
            bus_id=choice(buses).id
        )
        db.session.add(schedule)
    db.session.commit()

if __name__ == '__main__':
    delete_data()
    seed_roles()
    seed_users()
    seed_buses()
    seed_schedules()

    print("Database seeded successfully!")
