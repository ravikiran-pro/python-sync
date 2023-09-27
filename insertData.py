import time
from connection import products_collection

def insertProduct(data):
    try:
        if data == False:
            print(f"Nothing to Insert")
            return False

        print("Inserting....")
        # Insert the document into the products_collection
        insert_result = products_collection.insert_one(data)
        # Check if the insertion was successful
        if insert_result.acknowledged:
            print(f"Product inserted successfully. Inserted ID: {insert_result.inserted_id}")
        else:
            print(f"Failed to insert Product.")

    except Exception as e:
        print(f"Error insertProduct: {str(e)}")
        print(f"data: {data}")
        time.sleep(30)
        insertProduct(data)