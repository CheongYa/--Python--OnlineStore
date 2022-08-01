import pymongo

MONGO_URI = "mongodb+srv://Cheong:iCTbLJhGxxo6eOwG@cluster0.k0aktcy.mongodb.net/?retryWrites=true&w=majority"
MONGO_CONN = pymongo.MongoClient(MONGO_URI)

def conn_mongodb():
    db = MONGO_CONN.online_store
    test_connection = db.test_connection.insert_one({'test': 'test'})
    return db

conn_mongodb()