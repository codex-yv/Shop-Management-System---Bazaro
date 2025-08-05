from pymongo import MongoClient, UpdateOne

# MongoDB connection
mongo_uri = "your_mongo_uri_here"
client = MongoClient(mongo_uri)

# Access your database and collection
db = client["your_database_name"]
collection = db["your_collection_name"]

# Your data to update
update_data = {
    "p1": {"Quantity": 11},
    "p2": {"Quantity": 10}
}

# Prepare bulk operations (still one-liner-style, no for-loop from you)
operations = [
    UpdateOne({"_id": key}, {"$set": value}, upsert=True)
    for key, value in update_data.items()
]

# Execute all updates in one go
if operations:
    collection.bulk_write(operations)

print("Bulk update completed.")
