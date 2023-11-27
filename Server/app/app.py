from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Role, Bus, Schedule

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://your_username:your_password@localhost/your_database"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"
app.json['indent'] = 4
app.json['sort_keys'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Define your routes and API endpoints here

if __name__ == "__main__":
    app.run(port=5000, debug=True)
