from models import Bus, db, User, Driver, Booking, Schedule
from faker import Faker
from app import app
from random import choice as rc

faker = Faker()

with app.app_context():

    User.query.delete()
    Bus.query.delete()
    Driver.query.delete()
    Booking.query.delete()
    Schedule.query.delete()
    print("database cleared...")

# seed_User
    # your code here
    users = []

    #  seed_bus
    # your code here
    buses = []

    booking_data = []
    for i in range(20):
        bus_info = Bus(

            timestamp=faker.date_time_this_decade(),
            bus_id=rc(buses).id,
            user_id=rc(users).id
        )
        booking_data.append(bus_info)
    db.session.add_all(booking_data)
    print("booking data seeded")

    # bus_id
    # user_id


# seed_driver():

    schedule_data = []
    for i in range(20):
        data = Schedule(
            departure_time=faker.date_time_this_year(),
            route=rc("kasarani", "ruiru", "kimbo", "Toll", "Juja"),
            bus_id=rc(buses).id
        )
        schedule_data.append(data)
    db.session.add_all(schedule_data)
    db.session.commit()
    print("schedule data seeded")
    # bus_id  departure_time   route
