
from connection import client


def get_value(element):
    return element['value']

def updateSpecsData():
    productType = client.db['ProductType']
    products = client.db["Products"]
    productTypeData = productType.find({})
    for productType in productTypeData:
        specs = []
        options = {}
        optionsValue = {}
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
                print('completed --- ', product['brand'])
            print('completed product type --- ', product['brand'])
            for i in range(0, len(specs)):
                sorted = optionsValue[specs[i]]
                sorted.sort(key= get_value)
                productType['specifications'][i]['options'] = sorted
            print(productType['specifications'])                
