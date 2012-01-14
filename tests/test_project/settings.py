import os
PATH = os.path.dirname(os.path.abspath(__file__))

#Don't change this if you don't have renamed the project
PROJECT_NAME = "test_project"
PROJECT_ROOT = os.path.join(PATH, PROJECT_NAME)

DATABASE_ENGINE = 'sqlite'     #TODO: test elixir with several DB engines
DATABASE_NAME = 'test_project'
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''
DATABASE_PORT = ''

SHOW_DEBUG_INFO = True
