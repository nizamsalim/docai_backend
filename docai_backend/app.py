from dotenv import load_dotenv
load_dotenv()
from flask import Flask,jsonify
from .utils.config import Config
from .utils.db import db,migrate
from .controllers.auth_controller import auth_blueprint
from .utils.factory import register_error_handlers
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app,supports_credentials=True,origins=["http://localhost:5173"])

    db.init_app(app)
    migrate.init_app(app,db)

    register_error_handlers(app)

    from .models.user_model import User

    app.register_blueprint(auth_blueprint,url_prefix="/api/v1/auth")

    
    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)