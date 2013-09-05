====================================================
PyOdnoklassniki is an Odnoklassniki REST API wrapper
====================================================

This library consists of an API interface for `Odnoklassniki`_ and
Django middleware which helps to configure it.

Usage example:

.. code-block:: python

    import pyodnoklassniki


    pyodnoklassniki.app_pub_key = 'CBAJ...BABA'
    pyodnoklassniki.app_secret_key = '123...XYZ'

    ok_api = pyodnoklassniki.OdnoklassnikiAPI(
        access_token='kjdhfldjfhgldsjhfglkdjfg9ds8fg0sdf8gsd8fg')

    print ok_api.users.getCurrentUser()

.. _Odnoklassniki: http://odnoklassniki.ru
