import os 
PATH = os.path.dirname(os.path.abspath(__file__))

#Don't change this if you don't have renamed the project
PROJECT_NAME = "test_project"
PROJECT_ROOT = os.path.join(PATH, PROJECT_NAME)

DATABASE_ENGINE = 'postgres'     #TODO: test elixir with several DB engines
DATABASE_NAME = 'postgres'  
DATABASE_USER = 'postgres'             # Not used with sqlite3.
DATABASE_PASSWORD = '1234'         # Not used with sqlite3.
DATABASE_HOST = 'localhost'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '5432'     

SHOW_DEBUG_INFO = True
