from flask import Flask,make_response,request
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

class Index(Resource):
    def get(self):
        res = "welcome"
        return make_response(res,200)
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return user.serialize(), 200
        else:
            users = User.query.all()
            return [user.serialize() for user in users], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
        parser.add_argument('role', type=str, required=True, help='Role cannot be blank')
        args = parser.parse_args()

        new_user = User(**args)
        db.session.add(new_user)
        db.session.commit()
        return new_user.serialize(), 201

    def put(self, user_id):
        user = User.query.get_or_404(user_id)

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('role', type=str)
        args = parser.parse_args()

        user.update(args)
        db.session.commit()
        return user.serialize(), 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200

api.add_resource(Index, "/")
api.add_resource(UserResource, '/users', '/users/<int:user_id>')

if __name__=="__main__":
    app.run(port=5555,debug=True)