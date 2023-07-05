import os
import time
import threading
from pymongo import MongoClient
from dotenv import load_dotenv

MONGO_URI = os.getenv("MONGO_URI")

def insertProduct(data):
    try:
        if data == False:
            print(f"Nothing to Insert")
            return False

        # Connect to the MongoDB server
        client = MongoClient(MONGO_URI)

        # Access the database and collection
        db = client['prodkt-product-master-v1']
        collection = db['Products']

        # Define the filter to find the document to update
        filter = data.get('filter',{'model':data.get('model','')})

        # Checking whether the product is already in the DB or not
        isExist = collection.find_one(filter)

        if isExist is not None:
            print(f"Product Already Exists")
            print(f"Product Name: {data['name']}")
            print(f"Founded Product Name: {isExist['name']}")
        else:
            # Removing the filter key from data
            data.pop('filter')

            # Insert the document into the collection
            insert_result = collection.insert_one(data)

            # Check if the insertion was successful
            if insert_result.acknowledged:
                print(f"Product inserted successfully. Inserted ID: {insert_result.inserted_id}")
            else:
                print(f"Failed to insert Product.")

        # Close the connection
        client.close()

    except Exception as e:
        print(f"Error insertProduct: {str(e)}")
        print(f"data: {data}")
        time.sleep(30)
        threading.Thread(target=insertProduct,args=(data)).start()