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
    db = client['prodkt']
    collection = db['Products']

    # Define the filter to find the document to update
    filter = {'name': data['name']}

    isExist = collection.find_one(filter)

    if isExist is not None:
        print("Product Already Exists")
    else:
        # Insert the document into the collection
        insert_result = collection.insert_one(data)

        # Check if the insertion was successful
        if insert_result.acknowledged:
            print('Product inserted successfully. Inserted ID:', insert_result.inserted_id)
        else:
            print('Failed to insert Product.')

    # Close the connection
    client.close()
