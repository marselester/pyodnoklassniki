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

    try:
        print ok_api.users.getCurrentUser()
    except pyodnoklassniki.OdnoklassnikiError as exc:
        print exc

You might find that configuring library with Django Middleware is more
convenient.

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        # ...
        'pyodnoklassniki.contrib.django.middleware.PyOdnoklassnikiMiddleware',
        # ...
    )

    PYODNOKLASSNIKI = {
        'app_pub_key': 'CBAJ...BABA',
        'app_secret_key': '123...XYZ',
    }

Use dotted notation to invoke API method. Query parameters are passed as
keyword arguments. Odnoklassniki error codes are grouped by meaning in
``exceptions.py``, but ``OdnoklassnikiError`` might be enough.
See full list of API methods and error codes at  `Odnoklassniki API documentation`_.

.. code-block:: python

    try:
        response = ok_api.group.getUserGroupsV2()
    except pyodnoklassniki.OdnoklassnikiError as exc:
        print exc
    else:
        for group in response['groups']:
            print ok_api.group.getInfo(uids=group['groupId'],
                                       fields='name, description')

.. _Odnoklassniki: http://odnoklassniki.ru
.. _Odnoklassniki API documentation: http://apiok.ru/wiki/display/ok/Odnoklassniki+REST+API+ru
