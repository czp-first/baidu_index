import pymongo

client = pymongo.MongoClient(host="localhost", port=27017)
db = client["campus"]
collection = db["major"]


def get_names():

    items = collection.find({}, {"name": 1})
    names = []
    with open("major_names.txt", "a") as f:
        for item in items:
            f.write(item.get("name")[0])
            f.write("\n")


get_names()
