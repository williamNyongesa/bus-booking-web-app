from datetime import datetime
from flask import Flask, make_response, request, jsonify, session
from flask_migrate import Migrate
from models import db, User, Schedule, Bus
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)

# CORS(app, origins=["http://localhost:3000"], supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE"])
CORS(app, supports_credentials=True, origins=["http://localhost:3000"], methods=["GET", "POST", "PUT", "DELETE"])


app.secret_key = "b'\xd4\xfa\x1d\x0e\x02\x87\x91\x96V\xb5H{\xd3\xd5\x1ee'"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bbwa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
# CORS(app, origins="*")

# Parser for handling schedule data
schedule_parser = reqparse.RequestParser()
schedule_parser.add_argument("departure_place", type=str, required=True, help="Departure place is required.")
schedule_parser.add_argument("arrival_place", type=str, required=True, help="Arrival place is required.")
schedule_parser.add_argument("departure_time", type=str, required=True, help="Departure time is required.")
schedule_parser.add_argument("price", type=float, required=True, help="Price is required.")
schedule_parser.add_argument("bus_id", type=str, required=True, help="Bus ID is required.")


@app.before_request
def check_if_logged_in():
    exempted_endpoints = ["signup", "login", "users", "add_schedule", "delete_schedule"]

    if request.method != 'OPTIONS' and "user_id" not in session and request.endpoint not in exempted_endpoints:
        return {"error": "unauthorized access!"}, 401



class CheckSession(Resource):
    def get(self):
        if "user_id" in session:
            user = User.query.get(session["user_id"])
            if user:
                return user.to_dict(), 200

        return {"error": "User not logged in"}, 401


class Index(Resource):
    def get(self):
        res = "welcome"
        return make_response(res, 200)


class Signup(Resource):
    def post(self):
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password")

        if name and email and password:
            # Check if a user with the provided email already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {"error": "Email is already registered"}, 409

            # If the email is unique, create a new user
            new_user = User(name=name, email=email)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            user_data = new_user.to_dict()
            return {"user": user_data, "message": "User successfully created"}, 201

        return {"error": "Name, email, and password must be provided!"}, 422



class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            return user.to_dict(), 201

        return {"error": "Invalid credentials"}, 401


class Logout(Resource):
    def delete(self):
        if "user_id" in session:
            session.pop("user_id", None)
            return {"message": "Logout successful"}, 200
        else:
            return {"message": "User not logged in"}, 401


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        res = [user.to_dict() for user in users]
        return make_response(jsonify(res), 200)
    
class AddSchedule(Resource):
    def get(self):
        schedules = Schedule.query.all()
        res = [schedule.to_dict() for schedule in schedules]
        return make_response(jsonify(res), 200)
    
    def post(self):
        data = schedule_parser.parse_args()
        departure_place = data.get("departure_place")
        arrival_place = data.get("arrival_place")
        departure_time_str = data['departure_time']
        departure_time = datetime.strptime(departure_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        price = data.get("price")
        bus_id = data.get("bus_id")

        if departure_place and arrival_place and departure_time and price and bus_id:
            new_schedule = Schedule(
                departure_place=departure_place,
                arrival_place=arrival_place,
                departure_time=departure_time,
                price=price,
                bus_id=bus_id
            )

            db.session.add(new_schedule)
            db.session.commit()

            return {"message": "Schedule added successfully"}, 201

        return {"error": "All fields must be provided!"}, 422

    def options(self):
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.status_code = 200  # Set HTTP ok status for OPTIONS request
        return response


class EditSchedule(Resource):
    def put(self):
        data = schedule_parser.parse_args()
        schedule_id = request.json.get("id")
        departure_place = data.get("departure_place")
        arrival_place = data.get("arrival_place")
        departure_time_str = data['departure_time']
        departure_time = datetime.strptime(departure_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        price = data.get("price")
        bus_id = data.get("bus_id")

        if schedule_id and departure_place and arrival_place and departure_time and price and bus_id:
            schedule = Schedule.query.get(schedule_id)
            if schedule:
                schedule.departure_place = departure_place
                schedule.arrival_place = arrival_place
                schedule.departure_time = departure_time
                schedule.price = price
                schedule.bus_id = bus_id

                db.session.commit()

                return {"message": "Schedule updated successfully"}, 200
            else:
                return {"error": "Schedule not found"}, 404

        return {"error": "All fields must be provided!"}, 422

class DeleteSchedule(Resource):
    def delete(self):
        schedule_id = request.json.get("id")

        if schedule_id:
            schedule = Schedule.query.get(schedule_id)
            if schedule:
                db.session.delete(schedule)
                db.session.commit()

                return {"message": "Schedule deleted successfully"}, 200
            else:
                return {"error": "Schedule not found"}, 404

        return {"error": "Schedule ID must be provided!"}, 422
    

class SearchResults(Resource):
    def get(self):
        departure = request.args.get('departure')
        arrival = request.args.get('arrival')

        # Assuming you want to search for schedules in the ScheduleList
        schedules = Schedule.query.filter(
            Schedule.departure_place.ilike(f"%{departure}%"),
            Schedule.arrival_place.ilike(f"%{arrival}%")
        ).all()

        return [schedule.to_dict() for schedule in schedules]
    

class Bookings(Resource):
    def post(self):
        if "user_id" in session:
            user_id = session["user_id"]
            print(f"User ID: {user_id}")


            # Get user and schedule details from the request
            user = User.query.get(user_id)
            if user:
                data = request.json
                print(f"Received data: {data}")
                schedule_id = data.get("schedule_id")
                print(f"Schedule ID: {schedule_id}")

                # Assuming you have a relationship between User and Schedule models
                schedule = Schedule.query.get(schedule_id)
                if schedule:
                    # Check if the schedule is not already booked
                    if schedule not in user.bookings:
                        # Add the schedule to the user's bookings
                        user.bookings.append(schedule)
                        db.session.commit()

                        return {"message": "Booking created successfully"}, 201
                    else:
                        return {"error": "Schedule already booked"}, 400
                else:
                    return {"error": "Schedule not found"}, 404

        return {"error": "User not logged in"}, 401


class UserBookings(Resource):
    def get(self):
        if "user_id" in session:
            user_id = session["user_id"]
            user = User.query.get(user_id)
            if user:
                bookings = [booking.to_dict() for booking in user.bookings]
                return bookings, 200

        return {"error": "User not logged in"}, 401



class Buses(Resource):
    def get(self):
        buses = Bus.query.all()
        res = [bus.to_dict() for bus in buses]
        return make_response(jsonify(res), 200)

    def post(self):

        try:
            data = request.get_json()
            number_of_seats = data.get("number_of_seats")
            cost_per_seat = data.get("cost_per_seat")
            route = data.get("route")
            time_of_travel = data.get("time_of_travel")

            if number_of_seats and cost_per_seat and route and time_of_travel:
                new_bus = Bus(
                    number_of_seats=number_of_seats,
                    cost_per_seat=cost_per_seat,
                    route=route,
                    time_of_travel=time_of_travel,
                    user_id=session.get("user_id")  
                )

                db.session.add(new_bus)
                db.session.commit()

                return {"message": "Bus added successfully"}, 201

            return {"error": "All fields must be provided!"}, 422
        except Exception as e:
            print(f"Error in /buses POST: {e}")
            return {"error": "An unexpected error occurred"}, 500
    



api.add_resource(Index, "/")
api.add_resource(UserResource, "/users")
api.add_resource(CheckSession, "/session", endpoint="session")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(AddSchedule, "/add-schedule", endpoint="add_schedule")
api.add_resource(EditSchedule, "/edit-schedule", endpoint="edit_schedule")
api.add_resource(DeleteSchedule, "/delete-schedule", endpoint="delete_schedule")
api.add_resource(SearchResults, "/search-results", endpoint="search_results")
api.add_resource(Bookings, "/bookings")
api.add_resource(UserBookings, "/user-bookings")
api.add_resource(Buses, "/buses")




if __name__ == "__main__":
    app.run(port=5555, debug=True)
