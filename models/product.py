from email.errors import ObsoleteHeaderDefect
from .mongodb import conn_mongodb
from datetime import datetime
from bson import ObjectId

class Product():
    @staticmethod
    def insert_one(product, thumbnail_img_url, detail_img_url):
        db = conn_mongodb()
        db.products.insert_one({
            'name':product['name'],
            'price': product['price'],
            'description': product['description'],
            'thumbnail_img': thumbnail_img_url,
            'detail_img': detail_img_url,
            'user': 'admin',
            'created_at': int(datetime.now().timestamp()),
            'update_at': int(datetime.now().timestamp())
        })

    @staticmethod
    def find():
        db = conn_mongodb()
        products = db.products.find({})

        return products

    @staticmethod
    def delete_one(id):
        db = conn_mongodb()
        db.products.delete_one({'_id': ObjectId(id)})