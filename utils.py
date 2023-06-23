from bson import ObjectId
from datetime import datetime

current_datetime = datetime.now()
iso_string = current_datetime.isoformat()

def replace_all(text, old, new):
    while old in text:
        text = text.replace(old, new)
    return text

def giveMeProductRow(dataType,row):
    row['description'] = replace_all(row['description'],'\u00a0', '')
    row['model_name'] = replace_all(row['model_name'],'\u00a0', '')
    specifications = giveMeSpecification(dataType, row)
    newRow = {
        'name': row['model_name'],
        'brand': "",
        'model':"",
        'model_no': row.get('specs',{}).get('Model Number',""),
        'brand_image': row.get('brand_image',''),
        'description': row['description'],
        'warranty_coverage': row.get('specs',{}).get('Domestic Warranty',""),
        'warranty_details': {
            'warranty_summary': row.get('specs',{}).get('Warranty Summary',""),
            'covered':row.get('specs',{}).get('Covered in Warranty',""),
            'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
            'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
        },
        'img': row['images'][0] if row['images'] else 'https://prodkt-master.objectstore.e2enetworks.net/ProductPlaceholder.svg',
        'suggestion':"",
        'specifications': specifications,
        'category_id': "",
        'product_type_id':"",
        'is_active': True,
        'created_at': iso_string,
        'updated_at': iso_string,
        'scrap': row
    }

    if dataType == 'MOBILE':
        if specifications.get('RAM','') == '' and specifications.get('Storage','') == '':
            return False
        newRow['brand']= row['model_name'].split(' ')[0].strip()
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['category_id']= '61645a921082c438b19ad830'
        newRow['product_type_id']= '61645a921082c438b19ad835'
        newRow['suggestion']= row['model_name'].split('(')[0].strip() + ' ' + specifications['RAM'].replace(' ', '').lower()+' '+specifications['Storage'].replace(' ', '').lower() +' '+specifications['Color'].lower()
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.RAM': specifications.get('RAM','NA'),
            'specifications.Color': specifications.get('Color','NA'),
            'specifications.Storage': specifications.get('Storage','NA'),
        }
        return newRow

    if dataType == 'AC':
        if specifications.get('Type') not in ['Window', 'Split']:
            return False
        newRow['brand']= row.get('specs', {}).get('Brand',"")
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['category_id']= "61645a921082c438b19ad831"
        newRow['product_type_id']= "61645a921082c438b19ad844"
        newRow['suggestion']= row.get('specs', {}).get('Brand',"")+ ' ' + specifications["Type"]+' ac '+specifications["Capacity"].lower()
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Type': specifications.get('Type','NA'),
            'specifications.Inverter/Non-Inverter': specifications.get('Inverter/Non-Inverter','NA'),
            'specifications.Capacity': specifications.get('Capacity','NA'),
            'specifications.Rating': specifications.get('Rating','NA'),
        }
        return newRow
    
    if dataType == 'REFRIGERATOR':
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('model_name', {}).split(" L ")[0] + " L"
        newRow['model_no']= row.get('model_name', {}).split(",")[-1].strip()[:-1]
        newRow['category_id']= "61645a921082c438b19ad831"
        newRow['product_type_id']= "61645a921082c438b19ad841"
        newRow['warranty_coverage']= row.get('specs',{}).get('Warranty Summary',"").split('Warranty')[0].strip()
        newRow['suggestion']= newRow['brand'] + ' refrigerator ' + specifications["Capacity"].lower() + ' ' + specifications["Type"].lower() + ' ' + specifications["Rating"] + ' star'
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Type': specifications.get('Type','NA'),
            'specifications.Doors': specifications.get('Doors','NA'),
            'specifications.Capacity': specifications.get('Capacity','NA'),
            'specifications.Rating': specifications.get('Rating','NA'),
            'specifications.Color': specifications.get('Color','NA'),
        }
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

    if dataType == 'REFRIGERATOR':
        return {
            'Type': row.get('specs', {}).get('Type', ''),
            'Doors': row.get('specs', {}).get('Number of Doors', ''),
            'Capacity': row.get('specs', {}).get('Capacity', ''),
            'Rating': row.get('specs', {}).get('Star Rating', ''),
            'Color': row.get('model_name', {}).split("(")[1].split(",")[0]
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
    {
        "brands":[
            'LG', 'Samsung', 'Whirlpool', 'Haier', 'Godrej', 'Bosch', 'Panasonic', 'Voltas', 
            'Hitachi', 'IFB', 'Siemens', 'Kelvinator', 'Videocon', 'Onida', 'Toshiba', 'Electrolux', 
            'Sharp', 'Intex', 'Sansui', 'Mitashi', 'Blue Star', 'Croma', 'Lloyd', 'Kenstar'
        ],
        "searchKey":"refrigerator",
        "getRow": lambda row: giveMeProductRow('REFRIGERATOR',row)
    },
]

