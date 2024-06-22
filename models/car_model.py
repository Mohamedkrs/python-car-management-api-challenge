from database.db import db


class CarModel(db.Model):
    __tablename__ = 'car_models'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Car {self.make} {self.model}>'
