"""Custom exceptions for the controllers module."""


class NotFoundError(Exception):
    """Exception raised when a car is not found."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
