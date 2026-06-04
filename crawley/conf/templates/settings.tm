import os

PATH = os.path.dirname(os.path.abspath(__file__))

# Don't change this if you haven't renamed the project directory
PROJECT_NAME = "%(project_name)s"
PROJECT_ROOT = os.path.join(PATH, PROJECT_NAME)

# Configure your database here. Leave the fields empty (or remove them) if you
# don't want to use a relational database.
DATABASE_ENGINE = "sqlite"  # sqlite, postgres, mysql, oracle
DATABASE_NAME = "%(project_name)s"
DATABASE_USER = ""
DATABASE_PASSWORD = ""
DATABASE_HOST = ""
DATABASE_PORT = ""

# Document storages: set a filename to dump the scraped data.
XML_DOCUMENT = ""
JSON_DOCUMENT = ""
CSV_DOCUMENT = ""

# NoSQL storages (optional).
# MONGO_DB_HOST = "mongodb://localhost:27017"
# MONGO_DB_NAME = "%(project_name)s"
# COUCH_DB_HOST = "http://localhost:5984"
# COUCH_DB_NAME = "%(project_name)s"

# Maximum number of concurrent (asyncio) requests.
MAX_CONCURRENCY = 100

# Show general debug information
SHOW_DEBUG_INFO = True
