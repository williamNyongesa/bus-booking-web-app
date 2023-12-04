from flask import Flask, make_response, request, jsonify, session
from flask_migrate import Migrate
from models import db, User
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)

app.secret_key = "b'\xd4\xfa\x1d\x0e\x02\x87\x91\x96V\xb5H{\xd3\xd5\x1ee'"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bbwa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
CORS(app, origins="*")


@app.before_request
def check_if_logged_in():
    if "user_id" not in session and request.endpoint not in ["signup", "login", "users"]:
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
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if name and email and password:
            new_user = User(email=email, name=name)
            new_user.password_hash = password

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            return new_user.to_dict(), 201

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


api.add_resource(Index, "/")
api.add_resource(UserResource, "/users")
api.add_resource(CheckSession, "/session", endpoint="session")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")
api.add_resource(Logout, "/logout", endpoint="logout")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
