"""Database connectors building SQLAlchemy connection strings."""

import os.path

from crawley.utils import exit_with_error


class Connector:
    """Provides a SQLAlchemy connection string from the project settings."""

    def __init__(self, settings):
        self.settings = settings

    def get_connection_string(self):  # pragma: no cover - interface only
        raise NotImplementedError


class SimpleConnector(Connector):
    """Connector for file/host-less databases, e.g. sqlite."""

    def get_connection_string(self):
        path = getattr(self.settings, "PATH", "")
        return "sqlite:///%s" % os.path.join(path, self.settings.DATABASE_NAME)


class HostConnector(Connector):
    """Connector for databases requiring host, user and password."""

    def get_connection_string(self):
        user_pass = "%s:%s" % (
            self.settings.DATABASE_USER,
            self.settings.DATABASE_PASSWORD,
        )
        host_port = "%s:%s" % (
            self.settings.DATABASE_HOST,
            self.settings.DATABASE_PORT,
        )
        return "%s://%s@%s/%s" % (
            self.settings.DATABASE_ENGINE,
            user_pass,
            host_port,
            self.settings.DATABASE_NAME,
        )


class SqliteConnector(SimpleConnector):
    name = "sqlite"


class MySqlConnector(HostConnector):
    name = "mysql"


class OracleConnector(HostConnector):
    name = "oracle"


class PostgreConnector(HostConnector):
    name = "postgresql"

    def get_connection_string(self):
        # Accept the historical "postgres" engine name as well.
        self.settings.DATABASE_ENGINE = "postgresql"
        return super().get_connection_string()


class ConnectorsDict(dict):
    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        exit_with_error("Not a recognized database engine: %s" % key)


connectors = ConnectorsDict()
connectors.update(
    {
        "postgres": PostgreConnector,
        PostgreConnector.name: PostgreConnector,
        OracleConnector.name: OracleConnector,
        MySqlConnector.name: MySqlConnector,
        SqliteConnector.name: SqliteConnector,
    }
)
