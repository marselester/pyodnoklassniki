# coding: utf-8
"""
Django PyOdnoklassniki Middleware.

In order to install it add the following to your ``settings.py``:

- 'pyodnoklassniki.contrib.django.middleware.PyOdnoklassnikiMiddleware'
  to ``MIDDLEWARE_CLASSES``;
- Odnoklassniki application's credentials::

      PYODNOKLASSNIKI = {
          'app_pub_key': 'CBAJ...BABA',
          'app_secret_key': '123...XYZ',
      }

"""
import pyodnoklassniki
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings


class PyOdnoklassnikiMiddleware(object):

    def __init__(self):
        ok_settings = getattr(settings, 'PYODNOKLASSNIKI', {})

        if not ok_settings.get('app_pub_key'):
            raise MiddlewareNotUsed

        pyodnoklassniki.app_pub_key = ok_settings['app_pub_key']

        if 'app_secret_key' in ok_settings:
            pyodnoklassniki.app_secret_key = ok_settings['app_secret_key']
