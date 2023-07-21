
from connection import client
from bson import ObjectId


def get_value(element):
    return element['value']

def updateSpecsData():
    productType = client.db['ProductType']
    products = client.db["Products"]
    productTypeData = productType.find(
        {
            "_id": {
                '$in': [
                    ObjectId('61645a921082c438b19ad835'),
                    ObjectId('61645a921082c438b19ad844'),
                    ObjectId('61645a921082c438b19ad841'),
                    ObjectId('61645a921082c438b19ad845'),
                    ObjectId('61645a921082c438b19ad836'),
                    ObjectId('61645a921082c438b19ad838'),
                    ObjectId('61645a921082c438b19ad842'),
                    ObjectId('61645a921082c438b19ad83a'),
                    ObjectId('61645a921082c438b19ad846'),
                    ObjectId('61645a921082c438b19ad847')
                ]
            }
        }
    )
    collect = {}
    for productType in productTypeData:
        specs = []
        options = {}
        optionsValue = {}
        try:
            if(productType['specifications']):
                productData = products.find({'product_type_id': str(productType['_id'])})
                for specification in productType['specifications']:
                    specs.append(specification['value'])
                for product in productData:
                    if(product['specifications']):
                        for data in specs:
                            if(product['specifications'][data]):
                                if(data not in options):
                                    options[data] = []
                                    optionsValue[data] = []
                                if(product['specifications'][data] not in options[data]):
                                    options[data].append(product['specifications'][data])
                                    optionsValue[data].append(
                                        {
                                            "label": product['specifications'][data],
                                            "value": product['specifications'][data]
                                        }
                                    )
                collect[productType['_id']] = optionsValue
        except Exception as e:
            print(e)
    return optionsValue