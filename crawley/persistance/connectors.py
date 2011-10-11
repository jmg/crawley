"""
    Database connectors for elixir
"""
from crawley.manager.utils import exit_with_error

class Connector(object):
    """
        A Connector represents an object that can provide the
        database connection to the elixir framework.
    """
    
    def __init__(self, settings):
        
        self.settings = settings
        
    def get_connection_string(self):
        """
            Returns the connection string to the corresponding database
        """
        pass
        

class SimpleConnector(Connector):
    """
        A simple connector for a database without host and user. I.E: sqlite
    """
    
    def get_connection_string(self):        
        
        return "%s:///%s" % (self.settings.DATABASE_ENGINE, self.settings.DATABASE_NAME)


class HostConnector(Connector):
    """
        A connector for a database that requires host, user and password. I.E: postgres
    """

    def get_connection_string(self):
        
        user_pass = "%s:%s" % (self.settings.DATABASE_USER, self.settings.DATABASE_PASSWORD)
        host_port = "%s:%s" % (self.settings.DATABASE_HOST, self.settings.DATABASE_PORT)
        return "%s://%s@%s/%s" % (self.settings.DATABASE_ENGINE, user_pass, host_port, self.settings.DATABASE_NAME)                



class SqliteConnector(SimpleConnector):
    """
        Sqlite3 Engine connector
    """
    
    name = "sqlite"
    

class MySqlConnector(HostConnector):
    """
        Mysql Engine connector
    """
    
    name = "mysql"
    
    
class OracleConnector(HostConnector):
    """
        Oracle Engine connector
    """
    
    name = "oracle"
    
    
class PostgreConnector(HostConnector):
    """
        Postgre Engine connector
    """
    
    name = "postgres"
    

class ConnectorsDict(dict):
    
    def __getitem__(self, key):
        
        if key in self:
            return dict.__getitem__(self, key)
        else:
            exit_with_error("No recognized database Engine")
            

connectors = ConnectorsDict()
connectors.update({ PostgreConnector.name : PostgreConnector,
                    OracleConnector.name : OracleConnector,
                    MySqlConnector.name : MySqlConnector,
                    SqliteConnector.name : SqliteConnector})
