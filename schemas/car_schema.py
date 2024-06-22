import datetime

from marshmallow import Schema, fields, ValidationError, validates


class CarSchema(Schema):
    id = fields.Int(dump_only=True)
    make = fields.Str(required=True)
    model = fields.Str(required=True)
    year = fields.Int(required=True)
    price = fields.Float(required=True)

    @validates('year')
    def validate_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise ValidationError(f'Year cannot be greater than {current_year}')

    @validates('price')
    def validate_price(self, value):
        if value < 0:
            raise ValidationError('Price cannot be negative')


def validate(data):
    return None