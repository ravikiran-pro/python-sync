from pymongo import MongoClient

def insertProduct(data):

    if data == False:
        print('Nothing to Insert')
        return False

    # Connect to the MongoDB server
    client = MongoClient('mongodb://admin:VVD3lsuVl7TNbt5@91.203.132.255:27017/prodkt?directconnection=true')

    # Access the database and collection
    db = client['prodkt']
    collection = db['Products']

    # Define the filter to find the document to update
    filter = {'name': data['name']}

    # Define the update operation
    update = {'$set': data}

    # Perform the upsert operation
    result = collection.update_one(filter, update, upsert=True)

    # Check if the operation was successful
    if result.acknowledged:
        if result.upserted_id is not None:
            print('Document inserted:', result.upserted_id)
        else:
            print('Document updated:', result.modified_count)
    else:
        print('Failed to perform upsert operation.')

    # Close the connection
    client.close()
