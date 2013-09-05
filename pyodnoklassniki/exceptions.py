# coding: utf-8


class OdnoklassnikiError(Exception):
    """Base Odnoklassniki error class."""


class APIConnectionError(OdnoklassnikiError):
    """Network communication errors."""


class APIError(OdnoklassnikiError):
    """API server errors, e.g., specific error code or invalid response object.
    """

    ERROR_CODES = {
        1: 'UNKNOWN',
        2: 'SERVICE',
        9999: 'SYSTEM',
    }

    def __init__(self, message, http_content, http_status_code, json=None):
        super(APIError, self).__init__(message)
        self.message = message
        self.http_content = http_content
        self.http_status_code = http_status_code
        self.json = json


class AuthError(OdnoklassnikiError):
    """Authentication and authorization errors."""

    ERROR_CODES = {
        7: 'ACTION_BLOCKED',
        8: 'FLOOD_BLOCKED',
        9: 'IP_BLOCKED',
        10: 'PERMISSION_DENIED',
        11: 'LIMIT_REACHED',
        101: 'PARAM_API_KEY',
        102: 'PARAM_SESSION_EXPIRED',
        103: 'PARAM_SESSION_KEY',
        104: 'PARAM_SIGNATURE',
        105: 'PARAM_RESIGNATURE',
        200: 'PARAM_PERMISSION',
        210: 'PARAM_APPLICATION_DISABLED',
        401: 'AUTH_LOGIN',
        402: 'AUTH_LOGIN_CAPTCHA',
        453: 'SESSION_REQUIRED',
        455: 'FRIEND_RESTRICTION',
    }

    def __init__(self, message, http_content=None, http_status_code=None, json=None):
        super(AuthError, self).__init__(message)
        self.message = message
        self.http_content = http_content
        self.http_status_code = http_status_code
        self.json = json


class InvalidRequestError(OdnoklassnikiError, ValueError):
    """Invalid request parameters' errors."""

    ERROR_CODES = {
        3: 'METHOD',
        4: 'REQUEST',
        21: 'NOT_MULTIPART',
        100: 'PARAM',
        110: 'PARAM_USER_ID',
        120: 'PARAM_ALBUM_ID',
        130: 'PARAM_WIDGET',
        140: 'PARAM_MESSAGE_ID',
        300: 'NOT_FOUND',
        324: 'EDIT_PHOTO_FILE',
        454: 'CENSOR_MATCH',
        500: 'PHOTO_SIZE_LIMIT_EXCEEDED',
        501: 'PHOTO_SIZE_TOO_SMALL',
        502: 'PHOTO_SIZE_TOO_BIG',
        503: 'PHOTO_INVALID_FORMAT',
        504: 'PHOTO_IMAGE_CORRUPTED',
        505: 'PHOTO_NO_IMAGE',
        900: 'NO_SUCH_APP',
        1001: 'CALLBACK_INVALID_PAYMENT',
        1002: 'PAYMENT_IS_REQUIRED_PAYMENT',
        1003: 'INVALID_PAYMENT',
    }

    def __init__(self, message, http_content=None, http_status_code=None, json=None):
        super(InvalidRequestError, self).__init__(message)
        self.message = message
        self.http_content = http_content
        self.http_status_code = http_status_code
        self.json = json
