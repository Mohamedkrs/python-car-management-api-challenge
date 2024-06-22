from controllers.car_controller import CarController
from flask import Blueprint, request

from models.car_model import CarModel

car_bp = Blueprint('cars', __name__)


@car_bp.route('/', methods=['GET'])
def get_all_cars():
    return CarController.get_all_cars()


@car_bp.route('/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = CarModel.query.get_or_404(car_id)
    return car


@car_bp.route('/', methods=['POST'])
def create_car():
    data = request.get_json()
    return CarController.create_car(data)


@car_bp.route('/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    data = request.get_json()
    return CarController.update_car(car_id, data)


@car_bp.route('/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    return CarController.delete_car(car_id)
