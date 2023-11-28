from models import db, User, Role, Bus, Schedule
from faker import Faker
from app import app
from random import choice as rc
from random import uniform

fake = Faker()

with app.app_context():
    Role.query.delete()
    User.query.delete()
    Schedule.query.delete()
    Bus.query.delete()
    
    print("Database cleared and created...")

    # Seed Role
    my_roles = ['admin', 'user', 'driver']
    
    role_objects = [Role(name=role) for role in my_roles]
    db.session.add_all(role_objects)
    db.session.commit()
    print("Roles seeded!")

    # Seed User
    users = []
    for _ in range(20):
        user_info = User(
            email=fake.unique.email(),
            password="password123",  # Placeholder password
            role_id=rc(role_objects).id
            
        )
        users.append(user_info)
    db.session.add_all(users)
    db.session.commit()
    print("Users seeded!")

    

    # Seed Bus
    buses = []
    for _ in range(20):
        bus_info = Bus(
            number_of_seats=fake.random_int(min=20, max=60),
            cost_per_seat=uniform(10.0, 50.0),
            route=fake.word(),
            time_of_travel=fake.time(),
            user_id=rc(users).id
        )
        buses.append(bus_info)
    db.session.add_all(buses)
    db.session.commit()
    print("Buses seeded")

    # Seed Schedule
    schedule_data = []
    for i in range(20):
        data = Schedule(
            departure_time=fake.date_time_this_year(),
            bus_id=rc(buses).id
        )
        schedule_data.append(data)
    db.session.add_all(schedule_data)
    db.session.commit()
    print("Schedule data seeded")
