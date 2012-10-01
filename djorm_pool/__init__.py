from sqlalchemy import event
from sqlalchemy.pool import manage, QueuePool
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

import logging
from functools import partial

# Logging
log = logging.getLogger('djorm.pool')
_log = lambda msg, *args: log.debug(msg)

if settings.DEBUG:
    event.listen(QueuePool, 'checkout', partial(_log, 'retrieved from pool'))
    event.listen(QueuePool, 'checkin', partial(_log, 'returned to pool'))
    event.listen(QueuePool, 'connect', partial(_log, 'new connection'))


POOL_SETTINGS = getattr(settings, 'DJORM_POOL_OPTIONS', {})

try:
    from django.db.backends.postgresql_psycopg2 import base as pgsql_base
    pgsql_base._Database = pgsql_base.Database
    pgsql_base.Database = manage(pgsql_base._Database, **POOL_SETTINGS)
except ImproperlyConfigured:
    pass


try:
    from django.db.backends.mysql import base as mysql_base
    mysql_base._Database = mysql_base.Database
    mysql_base.Database = manage(mysql_base._Database, **POOL_SETTINGS)
except ImproperlyConfigured:
    pass


try:
    from django.db.backends.sqlite3 import base as sqlite3_base
    sqlite3_base._Database = sqlite3_base.Database
    sqlite3_base.Database = manage(sqlite3_base._Database, **POOL_SETTINGS)
except ImproperlyConfigured:
    pass
