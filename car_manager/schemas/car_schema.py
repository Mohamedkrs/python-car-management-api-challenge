"""Module for initializing the car schema."""

import datetime

from marshmallow import Schema, fields, validate


class CarSchema(Schema):
    """Schema for validating car data."""
    id = fields.Int(dump_only=True)
    make = fields.Str(required=True, validate=validate.Length(min=1),
                      error_messages={'required': 'Make is required and cannot be empty'})
    model = fields.Str(required=True,
                       error_messages={'required': 'Model is required and cannot be empty'})
    year = fields.Int(required=True, validate=validate.Range(min=1888, max=datetime.datetime.now().year),
                      error_messages={
                          'required': f'Year is required and cannot be greater than {datetime.datetime.now().year}'})
    color = fields.Str(required=True,
                       error_messages={'required': 'Color is required and cannot be empty'})
    price = fields.Float(required=True, validate=validate.Range(min=0),
                         error_messages={'required': 'Price is required and cannot be negative'})
