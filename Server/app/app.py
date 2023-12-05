from datetime import datetime
from flask import Flask, make_response, request, jsonify, session
from flask_migrate import Migrate
from models import db, User, Schedule
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from werkzeug.security import generate_password_hash


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


# Seed initial data including the admin user
def seed_initial_data():
    admin_user = User.query.filter_by(email="admin@example.com").first()
    if not admin_user:
        admin = User(
            name="Admin",
            email="admin@example.com",
            password=generate_password_hash("Adminpassword123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user created: {admin}")


with app.app_context():
    db.create_all()
    seed_initial_data()


# Parser for handling schedule data
schedule_parser = reqparse.RequestParser()
schedule_parser.add_argument("departure_place", type=str, required=True, help="Departure place is required.")
schedule_parser.add_argument("arrival_place", type=str, required=True, help="Arrival place is required.")
schedule_parser.add_argument("departure_time", type=str, required=True, help="Departure time is required.")
schedule_parser.add_argument("price", type=float, required=True, help="Price is required.")
schedule_parser.add_argument("bus_id", type=str, required=True, help="Bus ID is required.")


@app.before_request
def check_if_logged_in():
    exempted_endpoints = ["signup", "login", "users", "add_schedule", "edit_schedule", "delete_schedule", "admin_route", "driver_route"]

    if request.method != 'OPTIONS' and "user_id" not in session and request.endpoint not in exempted_endpoints:
        return {"error": "unauthorized access!"}, 401

    # Check user roles for admin and driver routes
    if request.endpoint in ["admin_route", "driver_route"]:
        user_id = session.get("user_id")
        if user_id:
            user = User.query.get(user_id)
            if user and user.role == "admin" and request.endpoint == "admin_route":
                return
            elif user and user.role == "driver" and request.endpoint == "driver_route":
                return
        return {"error": "unauthorized access for this role!"}, 401



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
    


class AdminDetailsResource(Resource):
    def get(self):
        if "user_id" in session:
            user_id = session["user_id"]
            user = User.query.get(user_id)
            if user and user.role == "admin":
                admin_details = {
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                }
                return jsonify(admin_details), 200
            else:
                return jsonify({"error": "User is not an admin"}), 403
        else:
            return jsonify({"error": "User not logged in"}), 401

class AdminRoute(Resource):
    def get(self):
        return {"message": "Admin route accessed"}

class DriverRoute(Resource):
    def get(self):
        return {"message": "Driver route accessed"}

class Signup(Resource):
    def post(self):
        name = request.json.get("name")
        email = request.json.get("email")
        password = request.json.get("password")

        role = request.json.get("role", "cleint")

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
            session["user_role"] = user.role  # Store the user role in the session
            return {"user": user.to_dict(), "role": user.role}, 201

            

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
        if "user_id" in session and session.get("user_role") == "admin":
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
            else:
                return {"error": "All fields must be provided!"}, 422
        else:
            return {"error": "Unauthorized access for this role!"}, 401

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

api.add_resource(Index, "/")
api.add_resource(UserResource, "/users")
api.add_resource(CheckSession, "/session", endpoint="session")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")
api.add_resource(AddSchedule, "/add-schedule", endpoint="add_schedule")
api.add_resource(EditSchedule, "/edit-schedule", endpoint="edit_schedule")
api.add_resource(DeleteSchedule, "/delete-schedule", endpoint="delete_schedule")
api.add_resource(AdminRoute, "/admin", endpoint="admin_route")  # Admin route
api.add_resource(DriverRoute, "/driver", endpoint="driver_route")  # Driver route
api.add_resource(AdminDetailsResource, "/admin-details")  # Admin details endpoint

if __name__ == "__main__":
    app.run(port=5555, debug=True)
