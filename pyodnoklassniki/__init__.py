# coding: utf-8
"""
PyOdnoklassniki is Odnoklassniki REST API wrapper.

Usage example::

    >>> import pyodnoklassniki
    >>> pyodnoklassniki.app_pub_key = 'CBAJ...BABA'
    >>> pyodnoklassniki.app_secret_key = '123...XYZ'
    >>> ok_api = pyodnoklassniki.OdnoklassnikiAPI(
    ...     access_token='kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg')
    >>> ok_api.users.getCurrentUser()

"""
from .requestor import APIRequestor, SessionAPIRequestor, OAuth2APIRequestor
from .exceptions import OdnoklassnikiError, AuthError, InvalidRequestError
from . import errors


app_pub_key = None
app_secret_key = None
api_base = 'http://api.odnoklassniki.ru/fb.do'


class OdnoklassnikiAPI(object):
    """Odnoklassniki API resource.

    Usage example for Non Session authentication::

        >>> ok_api = OdnoklassnikiAPI()

    Make sure that ``pyodnoklassniki.app_pub_key`` and
    ``pyodnoklassniki.app_secret_key`` are set.

    Usage example for Session authentication::

        >>> ok_api = OdnoklassnikiAPI(
        ...     session_secret_key='123...XYZ',
        ...     session_key='kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg')

    Make sure that ``pyodnoklassniki.app_pub_key`` is set.

    Usage example for OAuth 2.0 authentication::

        >>> ok_api = OdnoklassnikiAPI(
        ...     access_token='kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg')

    Make sure that ``pyodnoklassniki.app_pub_key`` and
    ``pyodnoklassniki.app_secret_key`` are set.

    Use dotted notation to invoke API method::

        >>> ok_api.users.getCurrentUser()
        >>> ok_api.group.getInfo(uids=123, fields='name,description')

    """

    _api_method_group = None
    _api_method_name = None
    _api_requestor = None

    def __init__(self, access_token=None, session_secret_key=None, session_key=None):
        self._access_token = access_token
        self._session_secret_key = session_secret_key
        self._session_key = session_key

    def __getattr__(self, name):
        is_method_magic = name.startswith('__')

        if not is_method_magic:
            if self._api_method_group is None:
                api = OdnoklassnikiAPI(self._access_token,
                                       self._session_secret_key,
                                       self._session_key)
                api._api_method_group = name
                # Caches ``api.api`` in order to reuse it.
                self.__dict__[name] = api
                return api

            if self._api_method_name is None:
                api = OdnoklassnikiAPI(self._access_token,
                                       self._session_secret_key,
                                       self._session_key)
                api._api_method_group = self._api_method_group
                api._api_method_name = name
                api._api_requestor = self._appropriate_api_requestor()
                # Caches ``api.api.api`` in order to reuse it.
                self.__dict__[name] = api
                return api

        raise AttributeError(
            "'OdnoklassnikiAPI' method's group, name have already been set"
        )

    def __call__(self, **query_params):
        if self._api_method:
            query_params['method'] = self._api_method
            return self._api_requestor.get(**query_params)
        else:
            raise TypeError("'OdnoklassnikiAPI' object is not callable")

    @property
    def _api_method(self):
        if self._api_method_group and self._api_method_name:
            return '{0}.{1}'.format(self._api_method_group, self._api_method_name)

    def _appropriate_api_requestor(self):
        if self._access_token:
            return OAuth2APIRequestor(
                app_pub_key=app_pub_key,
                app_secret_key=app_secret_key,
                access_token=self._access_token,
                api_base=api_base
            )
        if self._session_secret_key or self._session_key:
            return SessionAPIRequestor(
                app_pub_key=app_pub_key,
                session_secret_key=self._session_secret_key,
                session_key=self._session_key,
                api_base=api_base
            )
        return APIRequestor(
            app_pub_key=app_pub_key,
            app_secret_key=app_secret_key,
            api_base=api_base
        )
