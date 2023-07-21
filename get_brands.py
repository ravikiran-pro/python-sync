from utils import productData
from connection import brands, client

def getBrandsDetails():
    brandDetails = {}
    for product in productData:
        brandDetails[product['searchKey']] = {}
        for brand in product['brands']:
            filter = {'brand_id': brands[brand]['brand_id'],}
            count = client.getBrandCategoryCount(filter)
            brandDetails[product['searchKey']][brand] = count
    return brandDetails