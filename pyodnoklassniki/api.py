# coding: utf-8
from hashlib import md5

import requests

from .exceptions import APIConnectionError


API_BASE = 'http://api.odnoklassniki.ru/fb.do'


class APIRequestor(object):
    """Odnoklassniki API requestor.

    Usage example::

        >>> r = APIRequestor('app_pub_key', 'app_secret_key', 'access_token')
        >>> print r.get('users.getCurrentUser')

    """

    session = requests.Session()

    def __init__(self, app_pub_key, app_secret_key, access_token):
        self.app_pub_key = app_pub_key
        self.app_secret_key = app_secret_key
        self.access_token = access_token

    def get(self, method, method_params=None):
        params = {
            'method': method,
            'application_key': self.app_pub_key,
            'access_token': self.access_token,
            'format': 'JSON',
        }
        params['sig'] = self._oauth_signature(params)

        try:
            response = self.session.get(API_BASE, params=params)
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


class Odnoklassniki(object):
    """Odnoklassniki API resource.

    Usage example::

        >>> ok = Odnoklassniki('app_pub_key', 'app_secret_key', 'access_token')
        >>> print ok.users.getCurrentUser()

    """

    _api_method_group = None
    _api_method_name = None
    _cached_api_requestor = None

    def __init__(self, app_pub_key, app_secret_key, access_token):
        self.app_pub_key = app_pub_key
        self.app_secret_key = app_secret_key
        self.access_token = access_token

    def __getattr__(self, name):
        is_method_magic = name.startswith('__')

        if not is_method_magic:
            if self._api_method_group is None:
                api = Odnoklassniki(self.app_pub_key, self.app_secret_key,
                                    self.access_token)
                api._api_method_group = name
                return api

            if self._api_method_name is None:
                api = Odnoklassniki(self.app_pub_key, self.app_secret_key,
                                    self.access_token)
                api._api_method_group = self._api_method_group
                api._api_method_name = name
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

    @property
    def _api_requestor(self):
        if self._cached_api_requestor is None:
            self._cached_api_requestor = APIRequestor(self.app_pub_key,
                                                      self.app_secret_key,
                                                      self.access_token)
        return self._cached_api_requestor
