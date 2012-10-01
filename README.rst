djorm-ext-pool
==============

DB-API2 connection poolling for django.

Description
-----------

Is a simple application that uses the excellent SQLAlchemy connection pool to incorporate a connection pool for django. It's really very simple, making "monky patch" to the backends with sqlalchemy proxy object, which manages the pool. All work is based on https://github.com/kennethreitz/django-postgrespool/

**Note:** currently only been tested with postgresql, but in theory it should work perfectly with mysql and sqlite3.

You can add options to sqlalchemy connection pool adding them in the settings "DJORM_POOL_OPTIONS".

Example:

.. code-block:: python
    
    DJORM_POOL_OPTIONS = {
        "pool_size": 20, 
        "max_overflow":0
    }


How to install
--------------
Run ``python setup.py install`` to install, or place ``djorm_pool`` on your Python path.

You can also install it with: ``pip install djorm-ext-pool``

How use it?
-----------

Very simple, put ``djorm_pool`` in your ``INSTALLED_APPS`` settings:

.. code-block:: python
    
    # settings.py

    INSTALLED_APPS = (
        'djorm_pool',
        ...
    )
