# coding: utf-8
"""
PyOdnoklassniki is an Odnoklassniki REST API wrapper.

Usage example::

    >>> import pyodnoklassniki
    >>> pyodnoklassniki.app_pub_key = 'some app pub key'
    >>> pyodnoklassniki.app_secret_key = 'some app secret key'
    >>> access_token = 'kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg'
    >>> ok_api = pyodnoklassniki.OdnoklassnikiAPI(access_token)
    >>> ok_api.users.getCurrentUser()

"""
from hashlib import md5

import requests

from .exceptions import APIConnectionError


app_pub_key = None
app_secret_key = None
api_base = 'http://api.odnoklassniki.ru/fb.do'


class _OAuthAPIRequestor(object):
    """Odnoklassniki OAuth API requestor.

    Usage example::

        >>> access_token = 'kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg'
        >>> app_pub_key = 'CBAJ...BABA'
        >>> app_secret_key = '123...XYZ'
        >>> api_base = 'http://api.odnoklassniki.ru/fb.do'
        >>> r = _OAuthAPIRequestor(access_token, app_pub_key, app_secret_key,
        ...                        api_base)
        >>> r.get('users.getCurrentUser')

    """

    session = requests.Session()

    def __init__(self, access_token, app_pub_key, app_secret_key, api_base):
        self.access_token = access_token
        self.app_pub_key = app_pub_key
        self.app_secret_key = app_secret_key
        self.api_base = api_base

    def get(self, method, method_params=None):
        params = {
            'method': method,
            'access_token': self.access_token,
            'application_key': self.app_pub_key,
            'format': 'JSON',
        }
        params['sig'] = self._oauth_signature(params)

        try:
            response = self.session.get(self.api_base, params=params)
        except requests.RequestException as exc:
            raise APIConnectionError(exc.args[0])

        return response.json()

    def _oauth_signature(self, params):
        """Returns OAuth signature.

        Signature requirements:

        - parameters must not include ``access_token``;
        - parameters have to be sorted by name alphabetically;
        - string of parameters have to be in ``name1=value1name2=value2``
          format.

        Signature formula::

            md5(request_params_composed_string +
                md5(access_token + application_secret_key))

        """
        params_composed = sorted([
            '{}={}'.format(name, value)
            for name, value in params.iteritems() if name != 'access_token'
        ])

        postfix = md5(
            '{}{}'.format(self.access_token, self.app_secret_key)
        ).hexdigest()

        return md5(
            '{}{}'.format(''.join(params_composed), postfix)
        ).hexdigest()


class OdnoklassnikiAPI(object):
    """Odnoklassniki API resource.

    Usage example::

        >>> access_token = 'kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg'
        >>> ok_api = OdnoklassnikiAPI(access_token)
        >>> ok_api.users.getCurrentUser()

    Make sure that ``pyodnoklassniki.app_pub_key`` and
    ``pyodnoklassniki.app_secret_key`` are set.

    """

    _api_method_group = None
    _api_method_name = None
    _api_requestor = None

    def __init__(self, access_token):
        self._access_token = access_token

    def __getattr__(self, name):
        is_method_magic = name.startswith('__')

        if not is_method_magic:
            if self._api_method_group is None:
                api = OdnoklassnikiAPI(self._access_token)
                api._api_method_group = name
                # Caches ``api.api`` in order to reuse it.
                self.__dict__[name] = api
                return api

            if self._api_method_name is None:
                api = OdnoklassnikiAPI(self._access_token)
                api._api_method_group = self._api_method_group
                api._api_method_name = name
                api._api_requestor = _OAuthAPIRequestor(
                    access_token=self._access_token,
                    app_pub_key=app_pub_key,
                    app_secret_key=app_secret_key,
                    api_base=api_base
                )
                # Caches ``api.api.api`` in order to reuse it.
                self.__dict__[name] = api
                return api

        raise AttributeError(
            "{} method's group, name have already been set".format(type(self))
        )

    def __call__(self, **method_params):
        if self._api_method:
            return self._api_requestor.get(self._api_method, method_params)
        else:
            raise TypeError('{} object is not callable'.format(type(self)))

    @property
    def _api_method(self):
        if self._api_method_group and self._api_method_name:
            return '{}.{}'.format(self._api_method_group, self._api_method_name)
