from dotenv import load_dotenv

load_dotenv()
from flask import Flask, jsonify
from .utils.config import Config
from .utils.db import db, migrate
from .controllers.auth_controller import auth_blueprint
from .controllers.project_controller import project_blueprint
from .controllers.section_controller import section_blueprint
from .utils.error_handler import register_error_handlers
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    db.init_app(app)
    migrate.init_app(app, db)

    register_error_handlers(app)

    from .models.user_model import User
    from .models.project_model import Project
    from .models.section_model import Section
    from .models.refinement_model import Refinement

    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
    app.register_blueprint(project_blueprint, url_prefix="/api/v1/projects")
    app.register_blueprint(section_blueprint, url_prefix="/api/v1/sections")

    return app


app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
