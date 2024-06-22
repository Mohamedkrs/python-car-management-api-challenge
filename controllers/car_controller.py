from flask import jsonify
from flask_restful import fields, marshal_with

from database.db import db
from models.car_model import CarModel
from schemas.car_schema import CarSchema

resource_fields = {
    'id': fields.Integer,
    'make': fields.String,
    'model': fields.String,
    'year': fields.Integer,
    'color': fields.String,
    'price': fields.Float
}
car_schema = CarSchema()


class CarController:
    @staticmethod
    def get_all_cars():
        cars = CarModel.query.all()
        return cars

    @staticmethod
    def get_car(car_id):
        car = CarModel.query.get_or_404(car_id)
        return car

    @staticmethod
    @marshal_with(resource_fields)
    def create_car(data):
        errors = car_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        car = CarModel(
            make=data['make'],
            model=data['model'],
            year=data['year'],
            color=data['color'],
            price=data['price']
        )
        db.session.add(car)
        db.session.commit()
        return car, 201

    @staticmethod
    def update_car(car_id, data):
        errors = car_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        car = CarModel.query.get_or_404(car_id)
        car.make = data['make']
        car.model = data['model']
        car.year = data['year']
        car.color = data['color']
        car.price = data['price']
        db.session.commit()
        return car, 200

    @staticmethod
    def delete_car(car_id):
        car = CarModel.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        return '', 204
