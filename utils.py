from bson import ObjectId
from datetime import datetime

current_datetime = datetime.now()
iso_string = current_datetime.isoformat()

def replace_all(text, old, new):
    while old in text:
        text = text.replace(old, new)
    return text

def giveMeProductRow(dataType,row):
    row['description'] = replace_all(row['description'],'\u00a0', ' ')
    row['model_name'] = replace_all(row['model_name'],'\u00a0', ' ')
    specifications = giveMeSpecification(dataType, row)
    newRow = {
        'id': str(ObjectId()),
        'product_id': str(ObjectId()),
        'name': row['model_name'],
        'brand': "",
        'model':"",
        'description': row['description'],
        'img': row['images'][0] if row['images'] else 'https://prodkt-master.objectstore.e2enetworks.net/ProductPlaceholder.svg',
        'suggestion':"",
        'specifications': specifications,
        'category_id': "",
        'product_type_id':"",
        'is_active': True,
        'created_at': iso_string,
        'updated_at': iso_string
    }

    if dataType == 'MOBILE':
        if 'charger' in row['model_name'].lower():
            return False
        newRow['brand']= row['model_name'].split(' ')[0].strip()
        newRow['model']= row['model_name']
        newRow['category_id']= '61645a921082c438b19ad830'
        newRow['product_type_id']= '61645a921082c438b19ad835'
        newRow['suggestion']= row['model_name'].split('(')[0].strip() + ' ' + specifications['RAM'].replace(' ', '').lower()+' '+specifications['Storage'].replace(' ', '').lower() +' '+specifications['Color'].lower()
        return newRow

    if dataType == 'AC':
        if specifications.get('Type') not in ['Window', 'Split']:
            return False
        newRow['brand']= row.get('specs', {}).get('Brand',"")
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['category_id']= "61645a921082c438b19ad831"
        newRow['product_type_id']= "61645a921082c438b19ad844"
        newRow['suggestion']= row.get('specs', {}).get('Brand',"")+ ' ' + specifications["Type"]+' ac '+specifications["Capacity"].lower()
        return newRow


def giveMeSpecification(dataType, row):

    if dataType == 'MOBILE':
        return {
            'RAM': row.get('specs', {}).get('RAM', ''),
            'Storage': row.get('specs', {}).get('Internal Storage', ''),
            'Color': row.get('specs', {}).get('Color', '')
        }
    pass

    if dataType == 'AC':
        is_inverter = ' Inverter ' in row.get('model_name', '')
        return {
            'Type': row.get('specs', {}).get('Type', ''),
            'Inverter/Non-Inverter': 'Inverter' if is_inverter else 'Non-Inverter',
            'Capacity': row.get('specs', {}).get('Capacity in Tons', ''),
            'Rating': row.get('specs', {}).get('Star Rating', '')
        }
    pass

    return {}

productData = [
    {
        "brands":[ 
            "Acer", "Apple","Asus","BlackBerry","Celkon","Gionee","Google",
            "Haier","Honor","HP","HTC","Huawei","Infinix","Intex","Karbonn",
            "Lava","Lenovo","LG","Micromax","Microsoft","Motorola","Nokia","Nothing",
            "OnePlus","Oppo","Panasonic","Philips","Realme","Samsung","Sony",
            "Spice","TCL","Tecno","vivo","Xiaomi","XOLO","YU","ZTE"
        ],
        "searchKey":"mobiles",
        "getRow": lambda row: giveMeProductRow('MOBILE',row)
    },
    {
        "brands":[ 
            "Daikin","Voltas","Blue Star","LG","Hitachi","Carrier","Samsung","Whirlpool",
            "Godrej","Mitsubishi Electric","Panasonic","Lloyd","Haier","O General","Onida",
            "IFB","Sharp","TCL","Sanyo","Videocon"
        ],
        "searchKey":"ac",
        "getRow": lambda row: giveMeProductRow('AC',row)
    },
]

