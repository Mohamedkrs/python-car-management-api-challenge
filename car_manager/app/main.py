"""Module to run the Flask application."""

from flask import Flask

from car_manager.database.db import db
from car_manager.routes.car_routes import car_bp


def create_app(config_class=None):
    """Create and set up Flask api."""
    app = Flask(__name__)
    app.config.from_object(config_class or 'car_manager.config.Config')

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(car_bp, url_prefix='/api/cars')
    with app.app_context():
        db.create_all()
    return app


if __name__ == '__main__':
    from car_manager.config import DevelopmentConfig

    app = create_app(config_class=DevelopmentConfig)
    app.run()
