import os 

#Don't change this if you don't have renamed the project
PROJECT_NAME = "test_app"
PROJECT_ROOT = os.path.join(os.getcwd(), PROJECT_NAME)

DATABASE_ENGINE = 'sqlite'     #TODO: test elixir with several DB engines
DATABASE_NAME = 'test'  
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''     

SHOW_DEBUG_INFO = True
