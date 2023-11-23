from flask import Flask
from flask_migrate import Migrate
from models import db
from flask_restful import Resource,Api
from flask_cors import CORS

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///bbwa.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
CORS(app, origins="*")


if __name__=="__main__":
    app.run(port=5555,debug=True)