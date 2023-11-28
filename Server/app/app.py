from flask import Flask,make_response,request,jsonify,session
from flask_migrate import Migrate
from models import db
from flask_restful import Resource,Api,reqparse
from flask_cors import CORS
from models import User

app = Flask(__name__)

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

if __name__=="__main__":
    app.run(port=5555,debug=True)