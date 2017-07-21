# coding: utf-8
from hashlib import md5

import requests

from .exceptions import (
    APIConnectionError, APIError, AuthError, InvalidRequestError
)


session = requests.Session()


def json_api_response(api_url, query_params):
    try:
        response = session.get(api_url, params=query_params)
    except requests.RequestException as exc:
        raise APIConnectionError(
            message='Network communication error: {0}'.format(exc.args[0])
        )

    try:
        json_resp = response.json()
    except ValueError as exc:
        raise APIError(
            message='Invalid response object: {0}'.format(exc.args[0]),
            http_content=response.content,
            http_status_code=response.status_code
        )

    # Special case when API method returns empty list.
    if not json_resp:
        return json_resp

    if 'error_code' not in json_resp:
        return json_resp
    else:
        error_message = json_resp.get('error_msg')
        if json_resp['error_code'] in AuthError.CODES:
            raise AuthError(
                message=error_message,
                http_content=response.content,
                http_status_code=response.status_code,
                code=json_resp['error_code']
            )
        if json_resp['error_code'] in InvalidRequestError.CODES:
            raise InvalidRequestError(
                message=error_message,
                http_content=response.content,
                http_status_code=response.status_code,
                code=json_resp['error_code']
            )
        raise APIError(
            message=error_message,
            http_content=response.content,
            http_status_code=response.status_code,
            code=json_resp['error_code']
        )


class APIRequestor(object):
    """Odnoklassniki Non Session API requestor.

    Usage example::

        >>> app_pub_key = 'CBAJ...BABA'
        >>> app_secret_key = '123...XYZ'
        >>> api_base = 'http://api.odnoklassniki.ru/fb.do'
        >>> r = APIRequestor(app_pub_key, app_secret_key, api_base)
        >>> r.get(method='users.getCurrentUser')

    """

    def __init__(self, app_pub_key, app_secret_key, api_base):
        self.app_pub_key = app_pub_key
        self.app_secret_key = app_secret_key
        self.api_base = api_base

    def get(self, **query_params):
        query_params['application_key'] = self.app_pub_key
        query_params['format'] = 'JSON'
        query_params['sig'] = self._signature(query_params)

        return json_api_response(self.api_base, query_params)

    def _signature(self, params):
        """Returns signature.

        Signature requirements:

        - parameters have to be sorted by name alphabetically;
        - string of parameters have to be in ``name1=value1name2=value2``
          format.
        - calculated by formula::

              md5(request_params_composed_string + application_secret_key)

        """
        params_composed = ''
        for param_name in sorted(params):
            params_composed += '{0}={1}'.format(param_name, params[param_name])

        msg_byte = '{}{}'.format(params_composed, self.app_secret_key) \
            .encode('utf-8')
        sig = md5(msg_byte)
        return sig.hexdigest()


class SessionAPIRequestor(object):
    """Odnoklassniki Session API requestor.

    Usage example::

        >>> app_pub_key = 'CBAJ...BABA'
        >>> session_secret_key = '123...XYZ'
        >>> session_key = 'kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg'
        >>> api_base = 'http://api.odnoklassniki.ru/fb.do'
        >>> r = SessionAPIRequestor(app_pub_key, session_secret_key, session_key, api_base)
        >>> r.get(method='users.getCurrentUser')

    """

    def __init__(self, app_pub_key, session_secret_key, session_key, api_base):
        self.app_pub_key = app_pub_key
        self.session_secret_key = session_secret_key
        self.session_key = session_key
        self.api_base = api_base

    def get(self, **query_params):
        query_params['application_key'] = self.app_pub_key
        query_params['format'] = 'JSON'
        query_params['session_key'] = self.session_key
        query_params['sig'] = self._signature(query_params)

        return json_api_response(self.api_base, query_params)

    def _signature(self, params):
        """Returns signature.

        Signature requirements:

        - parameters have to be sorted by name alphabetically;
        - string of parameters have to be in ``name1=value1name2=value2``
          format.
        - calculated by formula::

              md5(request_params_composed_string + session_secret_key)

        """
        params_composed = ''
        for param_name in sorted(params):
            params_composed += '{0}={1}'.format(param_name, params[param_name])

        msg_byte = '{}{}'.format(params_composed, self.session_secret_key) \
            .encode('utf-8')
        sig = md5(msg_byte)
        return sig.hexdigest()


class OAuth2APIRequestor(object):
    """Odnoklassniki OAuth 2.0 API requestor.

    Usage example::

        >>> app_pub_key = 'CBAJ...BABA'
        >>> app_secret_key = '123...XYZ'
        >>> access_token = 'kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg'
        >>> api_base = 'http://api.odnoklassniki.ru/fb.do'
        >>> r = OAuth2APIRequestor(app_pub_key, app_secret_key, access_token, api_base)
        >>> r.get(method='users.getCurrentUser')

    """

    def __init__(self, app_pub_key, app_secret_key, access_token, api_base):
        self.app_pub_key = app_pub_key
        self.app_secret_key = app_secret_key
        self.access_token = access_token
        self.api_base = api_base

    def get(self, **query_params):
        query_params['application_key'] = self.app_pub_key
        query_params['format'] = 'JSON'
        query_params['access_token'] = self.access_token
        query_params['sig'] = self._signature(query_params)

        return json_api_response(self.api_base, query_params)

    def _signature(self, params):
        """Returns signature.

        Signature requirements:

        - parameters must not include ``access_token``;
        - parameters have to be sorted by name alphabetically;
        - string of parameters have to be in ``name1=value1name2=value2``
          format.
        - calculated by formula::

              md5(request_params_composed_string +
                  md5(access_token + application_secret_key))

        """
        params_composed = ''
        for param_name in sorted(params):
            if param_name == 'access_token':
                continue
            params_composed += '{0}={1}'.format(param_name, params[param_name])

        token_and_secret = md5(
            '{}{}'.format(self.access_token, self.app_secret_key).encode('utf-8')
        ).hexdigest()
        sig = md5(
            '{}{}'.format(params_composed, token_and_secret).encode('utf-8')
        )
        return sig.hexdigest()
