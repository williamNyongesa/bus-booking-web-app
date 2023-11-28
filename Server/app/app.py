from flask import Flask,make_response,request,jsonify,session
from flask_migrate import Migrate
from models import db
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS
from models import User

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///bbwa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
CORS(app, origins="*")

@app.before_request
def check_if_logged_in():
    if "user_id" not in session:
        if request.endpoint not in ["signup","login", "products"]:
            return {"error": "unauthorized access!"}, 401
class By_Id(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id==session['user_id']).first()

            # customer_dict = {
            #     "username": customer.username,
            #     "password": customer._password_hash
            # }
            return user.to_dict(), 200
        
        return {'error': 'Resource unavailable'}

class Index(Resource):
    def get(self):
        res = "welcome"
        return make_response(res,200)
    
class Signup(Resource):
    def post(self):
        email = request.get_json().get("email")
        password = request.get_json().get("password")

        if email and password:
            new_user = User(email=email, password=password)  # Set the password here
            # new_user.password_hash = password  # Remove this line

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            return new_user.to_dict(), 201

        return {"error": "Email and password must be provided!"}, 422

class Login(Resource):
    def post(self):
        email = request.get_json().get("email")
        password = request.get_json().get("password")

        user = User.query.filter(User.email == email).first()

        if user:
            if user.authenticate(password):
                session['user_id'] = user.id

                user_dict = user.to_dict()
                print("Login successful. User ID:", user.id)  
                return make_response(jsonify(user_dict), 201)
            else:
                print("Invalid password.")  
                return {"error": "Invalid password"}, 401
        
        print("User not registered.") 
        return {"error": "User not Registered"}, 404

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        res = [user.to_dict() for user in users]
        return make_response(
            jsonify(res),
            200)

    # def post(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
    #     parser.add_argument('role', type=str, required=True, help='Role cannot be blank')
    #     args = parser.parse_args()

    #     new_user = User(**args)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return new_user.serialize(), 201

    # def put(self, user_id):
    #     user = User.query.get_or_404(user_id)

    #     parser = reqparse.RequestParser()
    #     parser.add_argument('email', type=str)
    #     parser.add_argument('role', type=str)
    #     args = parser.parse_args()

    #     user.update(args)
    #     db.session.commit()
    #     return user.serialize(), 200

    # def delete(self, user_id):
    #     user = User.query.get_or_404(user_id)
    #     db.session.delete(user)
    #     db.session.commit()
    #     return {"message": "User deleted successfully"}, 200

api.add_resource(Index, "/")
api.add_resource(UserResource, '/users')
api.add_resource(By_Id, "/session", endpoint="session")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(Login, "/login", endpoint="login")

if __name__=="__main__":
    app.run(port=5555,debug=True)