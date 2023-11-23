from models import Bus, db, User, Driver, Booking, Schedule
from faker import Faker
from app import app
from random import choice as rc
from random import uniform

fake = Faker()

with app.app_context():
    User.query.delete()
    Bus.query.delete()
    Driver.query.delete()
    Booking.query.delete()
    Schedule.query.delete()
    print("Database cleared...")

    # Seed User
    users = []
    for _ in range(20):
        user_info = User(
            username=fake.user_name(),
            email=fake.unique.email(),
            role=fake.random_element(elements=('admin', 'user'))
        )
        users.append(user_info)
    db.session.add_all(users)
    db.session.commit()
    print("Users seeded!")

    # Seed Driver
    drivers = []
    for _ in range(20):
        driver = Driver(
            license_number=fake.unique.random_number(digits=8)
        )
        drivers.append(driver)
    db.session.add_all(drivers)
    db.session.commit()
    print("Drivers seeded")

    # Seed Bus
    buses = []
    for _ in range(20):
        bus_info = Bus(
            number_of_seats=fake.random_int(min=20, max=60),
            cost_per_seat=uniform(10.0, 50.0),
            route=fake.word(),
            time_of_travel=fake.time(),
            driver_id=rc(drivers).id
        )
        buses.append(bus_info)
    db.session.add_all(buses)
    db.session.commit()
    print("Buses seeded")

    # Seed Booking
    booking_data = []
    for i in range(20):
        booking_info = Booking(
            timestamp=fake.date_time_this_decade(),
            bus_id=rc(buses).id,
            user_id=rc(users).id
        )
        booking_data.append(booking_info)
    db.session.add_all(booking_data)
    db.session.commit()
    print("Booking data seeded")

    # Seed Schedule
    schedule_data = []
    for i in range(20):
        data = Schedule(
            departure_time=fake.date_time_this_year(),
            route=rc(["kasarani", "ruiru", "kimbo", "Toll", "Juja"]),
            bus_id=rc(buses).id
        )
        schedule_data.append(data)
    db.session.add_all(schedule_data)
    db.session.commit()
    print("Schedule data seeded")
