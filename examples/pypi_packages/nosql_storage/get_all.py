from pymongo.connection import Connection
import couchdb

connection = Connection("localhost")

db = connection.mongo_db_name

print "-" * 80
print "Mongo Entities"
print "-" * 80
print ""

for obj in db.Package.find():
    print obj

print "-" * 80
print ""
print "Total entities: %s" % db.Package.count()


print "-" * 80
print "CouchDb Entities"
print "-" * 80
print ""

couch = couchdb.Server("http://localhost:5984")
couch_db = "couch_db_name"

try:
    db = couch[couch_db]
except:
    db = couch.create(couch_db)

for entity in db:
    print db.get(entity)

print "-" * 80
print ""

print "Total entities: %s" % len(db)
