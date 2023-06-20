import os
from pymongo import MongoClient
from dotenv import load_dotenv

MONGO_URI = os.getenv("MONGO_URI")

def insertProduct(data):

    if data == False:
        print('Nothing to Insert')
        return False

    # Connect to the MongoDB server
    client = MongoClient(MONGO_URI)

    # Access the database and collection
    db = client['prodkt-product-master-v1']
    collection = db['Products']

    # Define the filter to find the document to update
    filter = data.get('filter',{'model':data.get('model','')})
    print('filter:', filter)

    # Checking whether the product is already in the DB or not
    isExist = collection.find_one(filter)
    print('isExist:', isExist)

    if isExist is not None:
        print("Product Already Exists")
    else:
        # Removing the filter key from data
        data.pop('filter')

        # Insert the document into the collection
        insert_result = collection.insert_one(data)

        # Check if the insertion was successful
        if insert_result.acknowledged:
            print('Product inserted successfully. Inserted ID:', insert_result.inserted_id)
        else:
            print('Failed to insert Product.')

    # Close the connection
    client.close()
