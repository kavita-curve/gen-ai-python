from flask import (
  Flask,
  jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    # Simple route
    @app.route('/')
    def hello_world(): 
        return jsonify({
           "status": "success",
            "message": "Hello World!"
        })

    return app