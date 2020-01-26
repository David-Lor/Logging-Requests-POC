"""EXCEPTIONS
Custom exceptions used by the application
"""

__all__ = ("NotFoundError",)


class NotFoundError(Exception):
    """The requested resource is not found (should return a 404 error)
    """
    def __init__(self, identifier):
        self.identifier = identifier
