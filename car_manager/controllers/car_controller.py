"""Module for handling car data and operations."""

from flask import jsonify
from flask_restful import fields, marshal_with
from sqlalchemy.exc import SQLAlchemyError

from car_manager.controllers.exceptions import NotFoundError, DBError
from car_manager.database.db import db
from car_manager.models.car_model import CarModel
from car_manager.schemas.car_schema import CarSchema

car_fields = {
    'id': fields.Integer,
    'make': fields.String,
    'model': fields.String,
    'year': fields.Integer,
    'color': fields.String,
    'price': fields.Float
}
car_schema = CarSchema()


class CarController:
    """Controller class for handling car data."""

    @staticmethod
    def get_car_from_db(car_id: int):
        """Get car by ID from database.

        :param car_id: ID of the car to fetch.
        :returns: Car object if found.
        :rtype: CarModel
        :raises NotFoundError: If car with ID is not found.
        """
        try:
            car = CarModel.query.get(car_id)
        except SQLAlchemyError as e:
            raise DBError(f"An error occurred while fetching car with id {car_id}: {str(e)}")
        if car is None:
            raise NotFoundError(f"Car with id {car_id} not found")
        return car

    @staticmethod
    def get_all_cars(page: int, per_page: int):
        """Get all cars from the database.

        :returns: A tuple containing the list of all cars and the HTTP status code.
        :rtype: list
        """
        try:
            cars = CarModel.query.paginate(page=page, per_page=per_page).items
            return marshal_with(car_fields)(lambda: cars)(), 200
        except SQLAlchemyError as e:
            return jsonify({"message": "An error occurred while fetching cars", "error": str(e)}), 500

    @staticmethod
    def get_car(car_id: int):
        """Fetch a car by its ID and return its details.

        :param int car_id: The unique identifier of the car to be fetched.
        :returns: A tuple containing the car details (or an error message) and the HTTP status code.
        :rtype: tuple
        """
        try:
            car = CarController.get_car_from_db(car_id)
        except NotFoundError as e:
            return jsonify({"message": e.message}), 404
        except SQLAlchemyError as e:
            return jsonify({"message": "An error occurred while fetching the car", "error": str(e)}), 500

        return marshal_with(car_fields)(lambda: car)(), 200

    @staticmethod
    def create_car(data: dict):
        """Create a new car and save it to the database.

        :param data: The car data to be saved.
        :return: A tuple containing the car details (or an error message) and the HTTP status code.
        :rtype: tuple
        """
        errors = car_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        car = CarModel(**data)
        try:
            db.session.add(car)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Database error", "error": str(e)}), 500

        return marshal_with(car_fields)(lambda: car)(), 201

    @staticmethod
    def update_car(car_id: int, data: dict):
        """Update a car's details in the database.

        :param car_id: The ID of the car to be updated.
        :param data: The new car data.
        :return: A tuple containing the updated car details (or an error message) and the HTTP status code.
        :rtype: tuple
        """
        errors = car_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        try:
            car = CarController.get_car_from_db(car_id)
        except NotFoundError as e:
            return jsonify({"message": e.message}), 404
        except SQLAlchemyError as e:
            return jsonify({"message": "An error occurred while fetching the car", "error": str(e)}), 500
        car = CarModel(**data)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred while updating the car", "error": str(e)}), 500
        return marshal_with(car_fields)(lambda: car)(), 200

    @staticmethod
    def delete_car(car_id: int):
        """Delete a car from the database.

        :param car_id: The ID of the car to be deleted.
        :return: A tuple containing an error message, in case of an error, and the HTTP status code.
        :rtype: tuple
        """
        try:
            car = CarController.get_car_from_db(car_id)
        except NotFoundError as e:
            return jsonify({"message": e.message}), 404
        try:
            db.session.delete(car)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred while deleting the car", "error": str(e)}), 500
        return '', 204
