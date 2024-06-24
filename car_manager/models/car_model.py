""" This module contains the CarModel class which is a model for the car_models table in the database."""
from car_manager.database.db import db


class CarModel(db.Model):
    """Car model for the car_models table."""
    __tablename__ = 'car_models'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Car {self.make} {self.model} {self.year}>'
