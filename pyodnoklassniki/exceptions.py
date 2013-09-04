# coding: utf-8


class OdnoklassnikiException(Exception):
    """Base exception class."""


class APIConnectionError(OdnoklassnikiException):
    """Network communication errors."""
