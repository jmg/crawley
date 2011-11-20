import os
PATH = os.path.dirname(os.path.abspath(__file__))

#Don't change this if you don't have renamed the project directory
PROJECT_NAME = "pypi"
PROJECT_ROOT = os.path.join(PATH, PROJECT_NAME)

#Configure you database here. If you don't want to use any leave the fields empty o remove them.
DATABASE_ENGINE = ''
DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

#If you want generate a XML o JSON document enter the name of the file here.
XML_DOCUMENT = ''
JSON_DOCUMENT = ''

MONGO_DB_HOST = 'localhost'
MONGO_DB_NAME = 'mongo_db_name'

COUCH_DB_HOST = 'http://localhost:5984'
COUCH_DB_NAME = 'couch_db_name'

#Show general debug information
SHOW_DEBUG_INFO = True

