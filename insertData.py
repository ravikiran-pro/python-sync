import time
from connection import products_collection

def insertProduct(data):
    try:
        if data == False:
            print(f"Nothing to Insert")
            return False

        # Define the filter to find the document to update
        filter = data.get('filter',{'model':data.get('PID','')})

        # Checking whether the product is already in the DB or not
        isExist = products_collection.find_one(filter)

        if isExist is not None:
            print(f"Product Already Exists: PID : {data['PID']}")
            print(f"Product Name: {data['name']}")
            print(f"Founded Product Name: {isExist['name']}")
        else:
            # Removing the filter key from data
            data.pop('filter')

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