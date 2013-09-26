# coding: utf-8
from . import errors


class OdnoklassnikiError(Exception):
    """Base Odnoklassniki error class."""


class APIConnectionError(OdnoklassnikiError):
    """Network communication errors."""

    def __init__(self, message):
        super(APIConnectionError, self).__init__(message)
        self.message = message


class APIError(OdnoklassnikiError):
    """API server errors, e.g., specific error code or invalid response object.
    """

    CODES = (
        errors.UNKNOWN,
        errors.SERVICE,
        errors.SYSTEM,
    )

    def __init__(self, message, http_content, http_status_code, code=None):
        super(APIError, self).__init__(message)
        self.message = message
        self.http_content = http_content
        self.http_status_code = http_status_code
        self.code = code


class AuthError(OdnoklassnikiError):
    """Authentication and authorization errors."""

    CODES = (
        errors.ACTION_BLOCKED,
        errors.FLOOD_BLOCKED,
        errors.IP_BLOCKED,
        errors.PERMISSION_DENIED,
        errors.LIMIT_REACHED,
        errors.PARAM_API_KEY,
        errors.PARAM_SESSION_EXPIRED,
        errors.PARAM_SESSION_KEY,
        errors.PARAM_SIGNATURE,
        errors.PARAM_RESIGNATURE,
        errors.PARAM_PERMISSION,
        errors.PARAM_APPLICATION_DISABLED,
        errors.AUTH_LOGIN,
        errors.AUTH_LOGIN_CAPTCHA,
        errors.SESSION_REQUIRED,
        errors.FRIEND_RESTRICTION,
    )

    def __init__(self, message, http_content=None, http_status_code=None, code=None):
        super(AuthError, self).__init__(message)
        self.message = message
        self.http_content = http_content
        self.http_status_code = http_status_code
        self.code = code


class InvalidRequestError(OdnoklassnikiError, ValueError):
    """Invalid request parameters' errors."""

    CODES = (
        errors.METHOD,
        errors.REQUEST,
        errors.NOT_MULTIPART,
        errors.PARAM,
        errors.PARAM_USER_ID,
        errors.PARAM_ALBUM_ID,
        errors.PARAM_WIDGET,
        errors.PARAM_MESSAGE_ID,
        errors.NOT_FOUND,
        errors.EDIT_PHOTO_FILE,
        errors.CENSOR_MATCH,
        errors.PHOTO_SIZE_LIMIT_EXCEEDED,
        errors.PHOTO_SIZE_TOO_SMALL,
        errors.PHOTO_SIZE_TOO_BIG,
        errors.PHOTO_INVALID_FORMAT,
        errors.PHOTO_IMAGE_CORRUPTED,
        errors.PHOTO_NO_IMAGE,
        errors.NO_SUCH_APP,
        errors.CALLBACK_INVALID_PAYMENT,
        errors.PAYMENT_IS_REQUIRED_PAYMENT,
        errors.INVALID_PAYMENT,
    )

    def __init__(self, message, http_content=None, http_status_code=None, code=None):
        super(InvalidRequestError, self).__init__(message)
        self.message = message
        self.http_content = http_content
        self.http_status_code = http_status_code
        self.code = code
