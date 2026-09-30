from django.apps import AppConfig
from django.db.backends.signals import connection_created


def configurar_sqlite(sender, connection, **kwargs):
    if connection.vendor != "sqlite":
        return

    with connection.cursor() as cursor:
        cursor.execute("PRAGMA busy_timeout = 30000")
        cursor.execute("PRAGMA journal_mode = WAL")
        cursor.execute("PRAGMA synchronous = NORMAL")


class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        connection_created.connect(
            configurar_sqlite,
            dispatch_uid="myapp.configurar_sqlite",
        )
