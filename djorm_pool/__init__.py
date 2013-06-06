# -*- coding: utf-8 -*-

from functools import partial

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy.pool import manage
from sqlalchemy.pool import Pool


# Activate logging on django debgu mode is ON
if settings.DEBUG:
    import logging
    log = logging.getLogger('djorm.pool')
    _log = lambda msg, *args: log.debug(msg)
    event.listen(Pool, 'checkout', partial(_log, 'retrieved from pool'))
    event.listen(Pool, 'checkin', partial(_log, 'returned to pool'))
    event.listen(Pool, 'connect', partial(_log, 'new connection'))


if getattr(settings, "DJORM_POOL_PESSIMISTIC", False):
    @event.listens_for(Pool, "checkout")
    def ping_connection(dbapi_connection, connection_record, connection_proxy):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("SELECT 1")
        except:
            # raise DisconnectionError - pool will try
            # connecting again up to three times before raising.
            raise exc.DisconnectionError()
        cursor.close()


POOL_SETTINGS = getattr(settings, 'DJORM_POOL_OPTIONS', {})
POOL_SETTINGS.setdefault("recycle", 3600)


def patch_mysql():
    class hashabledict(dict):
        def __hash__(self):
            return hash(tuple(sorted(self.items())))

    class hashablelist(list):
        def __hash__(self):
            return hash(tuple(sorted(self)))

    class ManagerProxy(object):
        def __init__(self, manager):
            self.manager = manager

        def __getattr__(self, key):
            return getattr(self.manager, key)

        def connect(self, *args, **kwargs):
            if 'conv' in kwargs:
                conv = kwargs['conv']
                if isinstance(conv, dict):
                    items = []
                    for k, v in conv.items():
                        if isinstance(v, list):
                            v = hashablelist(v)
                        items.append((k, v))
                    kwargs['conv'] = hashabledict(items)
            return self.manager.connect(*args, **kwargs)

    try:
        from django.db.backends.mysql import base as mysql_base
    except (ImproperlyConfigured, ImportError) as e:
        return

    if not hasattr(mysql_base, "_Database"):
        mysql_base._Database = mysql_base.Database
        mysql_base.Database = ManagerProxy(manage(mysql_base._Database, **POOL_SETTINGS))


def patch_postgresql():
    try:
        from django.db.backends.postgresql_psycopg2 import base as pgsql_base
    except (ImproperlyConfigured, ImportError) as e:
        return

    if not hasattr(pgsql_base, "_Database"):
        pgsql_base._Database = pgsql_base.Database
        pgsql_base.Database = manage(pgsql_base._Database, **POOL_SETTINGS)


def patch_sqlite3():
    try:
        from django.db.backends.sqlite3 import base as sqlite3_base
    except (ImproperlyConfigured, ImportError) as e:
        return

    if not hasattr(sqlite3_base, "_Database"):
        sqlite3_base._Database = sqlite3_base.Database
        sqlite3_base.Database = manage(sqlite3_base._Database, **POOL_SETTINGS)


def patch_all():
    patch_mysql()
    patch_postgresql()
    patch_sqlite3()


patch_all()
