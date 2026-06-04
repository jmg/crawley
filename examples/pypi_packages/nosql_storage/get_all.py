"""Dump the entities stored by the NoSQL example.

Requires ``pip install 'crawley[mongo]'`` for the Mongo part and a running
CouchDB server for the Couch part.
"""

import httpx
from pymongo import MongoClient

# -- MongoDB ---------------------------------------------------------------

connection = MongoClient("localhost")
db = connection.mongo_db_name

print("-" * 80)
print("Mongo Entities")
print("-" * 80)

for obj in db.Package.find():
    print(obj)

print("Total entities: %s" % db.Package.count_documents({}))


# -- CouchDB (plain HTTP API) ----------------------------------------------

couch = httpx.Client(base_url="http://localhost:5984")
couch_db = "couch_db_name"

couch.put("/%s" % couch_db)  # idempotent

print("-" * 80)
print("CouchDb Entities")
print("-" * 80)

rows = couch.get("/%s/_all_docs" % couch_db, params={"include_docs": "true"}).json()
for row in rows.get("rows", []):
    print(row["doc"])

print("Total entities: %s" % rows.get("total_rows", 0))
