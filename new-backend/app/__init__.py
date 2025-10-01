from flask import Flask
from flask_cors import CORS
from .config import get_config


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(get_config())

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .routes.health import bp as health_bp
    from .routes.users import bp as users_bp
    from .routes.mentorship import bp as mentorship_bp
    from .routes.opportunities import bp as opportunities_bp
    from .routes.stories import bp as stories_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(mentorship_bp, url_prefix="/api/mentorship")
    app.register_blueprint(opportunities_bp, url_prefix="/api/opportunities")
    app.register_blueprint(stories_bp, url_prefix="/api/stories")

    return app


