import os
from pymongo import MongoClient
MONGO_URI = os.getenv("MONGO_URI")

class Mongo():
    def __init__(self):
        # Connect to the MongoDB server
        self.client = MongoClient(MONGO_URI)

        # Access the database and collection
        self.db = self.client['prodkt-product-master-v1']

    def getProductsConnection(self):
        self.products_collection = self.db['Products']
        return self.products_collection

    def getBrandsList(self):
        brands_collection = self.db['Brands']
        brands = brands_collection.find({})
        data = {}
        for brand in brands:
            data[brand['name']] = {
                'name': brand['name'],
                'product_type_id': str(brand['product_type_id']),
                'category_id': str(brand['category_id']),
            } 
        self.brands = data
        return self.brands
    def Close(self):
        self.client.close()


client = Mongo()
products_collection = client.getProductsConnection()
brands = client.getBrandsList()
print(brands)