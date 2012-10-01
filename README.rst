djorm-ext-pool
==============

DB-API2 connection poolling for Django.

Description
-----------

Is a simple application that uses the excellent SQLAlchemy connection pool to incorporate a it to django. All work is based on https://github.com/kennethreitz/django-postgrespool/

**Note:** currently only been tested with postgresql, but in theory it should work perfectly with mysql and sqlite3.


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


You can add options to sqlalchemy connection pool adding them in the settings "DJORM_POOL_OPTIONS".

Example:

.. code-block:: python
    
    DJORM_POOL_OPTIONS = {
        "pool_size": 20, 
        "max_overflow":0
    }
