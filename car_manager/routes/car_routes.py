"""This module contains the routes for the car manager application."""

from flask import Blueprint, request

from car_manager.controllers.car_controller import CarController

car_bp = Blueprint('cars', __name__)


@car_bp.route('/', methods=['GET'])
def get_all_cars():
    """Get all cars from the database."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return CarController.get_all_cars(page, per_page)


@car_bp.route('/<int:car_id>', methods=['GET'])
def get_car(car_id: int):
    """Fetch a car by its ID and return its details."""
    return CarController.get_car(car_id)


@car_bp.route('/', methods=['POST'])
def create_car():
    """Create a new car and save it to the database."""
    data = request.get_json()
    return CarController.create_car(data)


@car_bp.route('/<int:car_id>', methods=['PUT'])
def update_car(car_id: int):
    """Update a car's details in the database."""
    data = request.get_json()
    return CarController.update_car(car_id, data)


@car_bp.route('/<int:car_id>', methods=['DELETE'])
def delete_car(car_id: int):
    """Delete a car from the database."""
    return CarController.delete_car(car_id)
