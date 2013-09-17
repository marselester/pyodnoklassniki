# coding: utf-8
"""
The Odnoklassniki signature calculator is very helpful
http://www.glowfall.ru/calc_sig/

"""
try:
    import unittest2 as unittest
except ImportError:
    import unittest
import mock

from pyodnoklassniki.requestor import (
    APIRequestor, SessionAPIRequestor, OAuth2APIRequestor, json_api_response
)
from pyodnoklassniki import AuthError, errors
from .utils import MockResponse


class APIRequestorSignatureTest(unittest.TestCase):

    def test_signature(self):
        requestor = APIRequestor(app_pub_key='app key',
                                 app_secret_key='app secret key',
                                 api_base='whatever')
        params = {
            'application_key': 'app key',
            'method': 'users.getCurrentUser'
        }
        signature = requestor._signature(params)
        expected_signature = 'a6a34ee469a3aa62199c9d174966c7c8'

        self.assertEqual(signature, expected_signature)


class SessionAPIRequestorSignatureTest(unittest.TestCase):

    def test_signature(self):
        requestor = SessionAPIRequestor(app_pub_key='app key',
                                        session_secret_key='session secret key',
                                        session_key='session key',
                                        api_base='whatever')
        params = {
            'application_key': 'app key',
            'method': 'users.getCurrentUser',
            'session_key': 'session key',
        }
        signature = requestor._signature(params)
        expected_signature = 'cb30c5ea3e44779299dbc90e81bd3d36'

        self.assertEqual(signature, expected_signature)


class OAuth2APIRequestorSignatureTest(unittest.TestCase):

    def test_signature(self):
        requestor = OAuth2APIRequestor(app_pub_key='app key',
                                       app_secret_key='app secret key',
                                       access_token='access token',
                                       api_base='whatever')
        params = {
            'application_key': 'app key',
            'method': 'users.getCurrentUser',
            'access_token': 'access token',
        }
        signature = requestor._signature(params)
        expected_signature = '8a41a73bcef600b6a3464158b2059549'

        self.assertEqual(signature, expected_signature)


class JSONAPIResponseTest(unittest.TestCase):

    @mock.patch('pyodnoklassniki.requestor.session.get', autospec=True)
    def test_auth_error_when_server_returns_invalid_session_key_error(self, r_get):
        content = """{
            "error_code": 103,
            "error_data": null,
            "error_msg": "PARAM_SESSION_KEY : Invalid session key"
        }
        """
        r_get.return_value = MockResponse(content)

        with self.assertRaises(AuthError) as cm:
            json_api_response(api_url='blah', query_params={})

        self.assertEqual(cm.exception.code, errors.PARAM_SESSION_KEY)
