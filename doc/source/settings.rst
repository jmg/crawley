Settings File
-----------------------------------

The settings.py file is required in every crawley's project.
A common settings file looks like this:

.. code-block:: python

    import os 
    PATH = os.path.dirname(os.path.abspath(__file__))

    #Don't change this if you don't have renamed the project
    PROJECT_NAME = "test_project"
    PROJECT_ROOT = os.path.join(PATH, PROJECT_NAME)

    DATABASE_ENGINE = 'postgres'     
    DATABASE_NAME = 'postgres'  
    DATABASE_USER = 'postgres'         
    DATABASE_PASSWORD = '1234'         
    DATABASE_HOST = 'localhost'             
    DATABASE_PORT = '5432'     

    SHOW_DEBUG_INFO = True


.. warning:: Don't change the PROJECT_NAME constant if you don't have renamed the project on your filesystem.

The SHOW_DEBUG_INFO constant indicates if you want to log the crawling results
to the stdout.

Configure your database
=======================

The settings file provides you the capability for configure your database engine.
The followings are configuration examples for the database engines supported so far.

Sqlite 
========

It doesn't support host and user parameters. So, set it to empty.

.. note:: Requires sqlite3 module

.. code-block:: python

    DATABASE_ENGINE = 'sqlite'     
    DATABASE_NAME = 'my_data_base'  
    DATABASE_USER = ''             
    DATABASE_PASSWORD = ''         
    DATABASE_HOST = ''             
    DATABASE_PORT = ''    

MySql 
========

.. note:: Requires MySQLdb module

.. code-block:: python

    DATABASE_ENGINE = 'mysql'     
    DATABASE_NAME = 'my_data_base'  
    DATABASE_USER = 'mysql_user'             
    DATABASE_PASSWORD = 'xxxxx'         
    DATABASE_HOST = 'localhost'             
    DATABASE_PORT = '3306'   

Postgres
========

.. note:: Requires psycopg2 module

.. code-block:: python

    DATABASE_ENGINE = 'postgres'     
    DATABASE_NAME = 'my_data_base'  
    DATABASE_USER = 'postgres_user'        
    DATABASE_PASSWORD = 'xxxxx'        
    DATABASE_HOST = 'localhost'             
    DATABASE_PORT = '5432'  
    
Oracle 
========

.. note:: Requires cx_Oracle module

.. code-block:: python

    DATABASE_ENGINE = 'oracle'     
    DATABASE_NAME = 'my_data_base'  
    DATABASE_USER = 'oracle_user'             
    DATABASE_PASSWORD = 'xxxxx'         
    DATABASE_HOST = 'localhost'             
    DATABASE_PORT = '1521'   
