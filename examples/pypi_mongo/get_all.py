from pymongo.connection import Connection
connection = Connection("localhost")

db = connection.sarasa

for obj in db.Packages.find():
    print obj

print db.Package.count()
