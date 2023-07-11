from datetime import datetime
from connection import brands

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
        'category_id': brands[row['brand_name']]['category_id'],
        'product_type_id': brands[row['brand_name']]['product_type_id'],
        'brand_id': brands[row['brand_name']]['brand_id'],
        'PID': row['pid'],
        'is_active': True,
        'created_at': iso_string,
        'updated_at': iso_string,
        'scrap': None
    }

    if dataType == 'MOBILE':
        if specifications.get('RAM','') == '' and specifications.get('Storage','') == '':
            return False
        newRow['brand']= row['model_name'].split(' ')[0].strip()
        newRow['model']= row.get('specs', {}).get('Model Name',"")
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
        if specifications.get('Type','') == '' and specifications.get('Doors','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('model_name', {}).split(" L ")[0] + " L"
        newRow['model_no']= row.get('model_name', {}).split(",")[-1].strip()[:-1]
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


    if dataType == 'TV':    
        if specifications.get('Type','') == '' and specifications.get('Size','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('model_name', {}).split(" (", 1)[0]
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['model_no']= newRow['model_no'][0] or row.get('specs', {}).get('Model Name',"")
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        resolution = specifications['Resolution'].lower()
        if (resolution):
            resolution = resolution[:1]
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= row.get('model_name', {}).split(" ")[0] + ' ' + specifications['Type'].replace(' ', '').lower()+' '+specifications['Size'].replace(' ', '').lower() +' '+resolution
        newRow['filter'] = {
            'model_no': newRow['model_no'],
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Type': specifications.get('Type','NA'),
            'specifications.Size': specifications.get('Size','NA'),
            'specifications.Resolution': resolution or 'NA',
        }
        return newRow

    if dataType == 'LAPTOP':    
        if specifications.get('Ram','') == '' and specifications.get('Processor','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',""),
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['model_no']= newRow['model_no'][0] or row.get('specs', {}).get('Model Name',"")
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= row.get('model_name', {}).split(" ")[0] + ' ' + specifications['Os'].replace(' ', '').lower()+' '+specifications['Processor'].replace(' ', '').lower() +' '+specifications['Ram'].lower()
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Os': specifications.get('Operating System','NA'),
            'specifications.Processor': specifications.get('Processor Name','NA'),
            'specifications.Ram': specifications.get('Ram','NA'),
        }
        return newRow
    
    if dataType == 'TABLET':    
        if specifications.get('RAM','') == '' and specifications.get('Storage','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['model_no']= newRow['model_no'][0] or row.get('specs', {}).get('Model Name',"")
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= newRow['brand'].split('(')[0].strip() + ' ' + specifications['RAM'].replace(' ', '').lower()+' '+specifications['Storage'].replace(' ', '').lower() +' '+specifications['Color'].lower()
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.RAM': specifications.get('RAM','NA'),
            'specifications.Storage': specifications.get('Internal Storage','NA'),
            'specifications.Color': specifications.get('Color','NA'),
        }
        return newRow
    
    if dataType == 'WASHING MACHINE':    
        if specifications.get('Load','') == '' and specifications.get('Capacity','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['model_no']= newRow['model_no'][0] or row.get('specs', {}).get('Model Name',"")
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= newRow['brand'].split('(')[0].strip() + ' ' + specifications['Load'].replace(' ', '').lower()+' '+specifications['Capacity'].replace(' ', '').lower() +' '+specifications['Color'].lower()
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Load': specifications.get('Function Type','NA'),
            'specifications.Capacity': specifications.get('Washing Capacity','NA'),
            'specifications.Color': specifications.get('Color','NA'),
        }
        return newRow
    
    if dataType == 'PRINTER SCANNERS':    
        if specifications.get('Type','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['model_no']= newRow['model_no'][0] or row.get('specs', {}).get('Model Name',"")
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= newRow['brand'].split('(')[0].strip() + ' ' + specifications['Type'].replace(' ', '').lower()
        newRow['filter'] = {
            # 'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Type': specifications.get('Printing Method','NA'),
        }
        return newRow
    
    if dataType == 'CHIMNEY':  
        if specifications.get('Mount_type','') == '':
            return False  
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['model_no']= newRow['model_no'][0] or row.get('specs', {}).get('Model Name',"")
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= newRow['brand'].split('(')[0].strip() + ' ' + specifications['Mount_type'].replace(' ', '').lower()+' '+specifications['Color'].replace(' ', '').lower()
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Mount_type': specifications.get('Mount_type','NA'),
            'specifications.Color': specifications.get('Color','NA'),
        }
        return newRow

    
    if dataType == 'WATER PURIFIER': 
        if specifications.get('Capacity','') == '':
            return False     
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['model_no']= newRow['model_no'][0] or row.get('specs', {}).get('Model Name',"")
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= newRow['brand'].split('(')[0].strip() + ' ' + specifications['Capacity'].replace(' ', '').lower()+' '+specifications['Color'].replace(' ', '').lower()
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Capacity': specifications.get('Total Capacity','NA'),
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

    if dataType == 'TV':
        return {
            'Type': row.get('specs', {}).get('Screen Type', ''),
            'Size': row.get('specs', {}).get('Display Size', ''),
            'Resolution': row.get('specs', {}).get('HD Technology & Resolution', '').split(",")[1]
        }
    pass

    if dataType == 'LAPTOP':
        return {
            'Os': row.get('specs', {}).get('Operating System', ''),
            'Processor': row.get('specs', {}).get('Processor Name', ''),
            'Ram': row.get('specs', {}).get('RAM', ''),
        }
    pass

    if dataType == 'TABLET':
        return {
            'RAM': row.get('specs', {}).get('RAM', ''),
            'Storage': row.get('specs', {}).get('Internal Storage', ''),
            'Color': row.get('specs', {}).get('Color', ''),
        }
    pass

    if dataType == 'WASHING MACHINE':
        return {
            'Load': row.get('specs', {}).get('Function Type', ''),
            'Capacity': row.get('specs', {}).get('Washing Capacity', ''),
            'Color': row.get('specs', {}).get('Color', ''),
        }
    pass


    if dataType == 'PRINTER SCANNERS':
        return {
           'Type': row.get('specs', {}).get('Printing Method', ''),
        }
    pass

    if dataType == 'CHIMNEY':
        return {
           'Mount_type': row.get('specs', {}).get('Mount Type', ''),
           'Color': row.get('specs', {}).get('Color', ''),
        }
    pass


    if dataType == 'WATER PURIFIER':
        return {
           'Capacity': row.get('specs', {}).get('Total Capacity', ''),
           'Color': row.get('specs', {}).get('Color', ''),
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
        "searchKey":"mobile",
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
    {
        "brands":[
            'Samsung', 'Haier', 'Panasonic','Onida',
            'Toshiba', 'Intex', 'Lloyd', 'realme', 'Mi',
            'OnePlus', 'Sony', 'Vu', 'Thomson', 'Motorola',
            'Infinix', 'Tcl', 'Iffalcon', 'Acer', 'Micromax',
            'Nokia',  'Philips', 'Bpl', 'Itel',
        ],
        "searchKey":"tv",
        "getRow": lambda row: giveMeProductRow('TV',row)
    },
    {
        "brands":[
            'Hp', 'Asus', 'Lenovo', 'Dell', 'Msi',
            'Apple', 'Avita', 'Acer', 'Samsung', 'Infinix',
            'Realme', 'Gigabyte', 'Vaio', 'Primebook', 'Alienware',
            'Smartron', 'Microsoft', 'Lg Gram',  
        ],
        "searchKey":"laptop",
        "getRow": lambda row: giveMeProductRow('LAPTOP',row)
    },
    {
        "brands":[
            'Honor', 'Mi', 'OnePlus', 'Oppo', 'Apple',
            'Spigen', 'Samsung', 'Lenovo', 'Huawei', 'Asus',
            'Xiaomi', 'Dell', 'HP', 'Google', 'Tcl',
            'Alcatel', 'Iball', 'Honor', 'Motorola',
              ],
        "searchKey":"tablet",
        "getRow": lambda row: giveMeProductRow('TABLET',row)
    },
    {
        "brands":[
             'Samsung', 'LG', 'Whirlpool', 'IFB', 'Panasonic', 
             'Motorola', 'Thomson', 'Godrej', 'Bosch', 'Voltas beko', 
             'Haier', 'Lloyd', 'Onida', 
              ],
        "searchKey":"washing machine",
        "getRow": lambda row: giveMeProductRow('WASHING MACHINE',row)
    },
    {
        "brands":[
             'HP', 'Epson', 'Canon', 'brother', 'PANTUM',
             'Xerox', 'SAMSUNG', 
              ],
        "searchKey":"printer scanners",
        "getRow": lambda row: giveMeProductRow('PRINTER SCANNERS',row)
    },
    {
        "brands":[
             'Elica', 'Faber', 'Hindware', 'Glen', 'Sunflame',
             'Prestige', 'Kaff', 'Bosch', 'Inalsa', 'Kutchina', 
             'V-Guard',        
               ],
        "searchKey":"Chimney",
        "getRow": lambda row: giveMeProductRow('CHIMNEY',row)
    },
    {
        "brands":[
             'Aquaguard', 'Pureit', 'Hindware', 'Blue Star', 'LG',
             'AquaDpure', 'AQUA', 'Aqua Fresh', 'Fedula', 'KENT',
             'Aqua Dove', 'Remino', 'NPT Purification System', 'Keel', 'Grand plus',
             'Royal Aquafresh', 'Aquafresh', 'Kaveri AquaFresh', 'E.F.M', 'AquaDart',
             'G.S. Aquafresh', 'Hydroshell', 'Blair', 'Aqua Ace', 'Earth', 
             'LIVPURE', 'Aquaultra', 'Havells', 'Aquamart', 'Always', 
             'GE Filtration', 'AquaActive', 'Aquanza', 'Aqua Nerio', 'Purosis', 
             'Earth Ro System', 'ONE RO', 'Muskpure', 'Star Aqua', 'Blueshell', 
             'V-Guard', 'Trypkon', 'AO Smith', 'One7', 'MarQ by Flipkart', 
             'AQUA KING', 'TSP AQUA', 'OneTech', 'Aqua Active', 'Tata Swach', 
             'PureOne', 'Nexus Pure', 'Mclord', 'Safex', 'Noir Aqua', 
             'Eureka Forbes Ltd', 'Apeiron', 'Oseas Aqua', 'Aquadfresh', 'Rama', 
             'R.K. Aqua Fresh India', 'NILE', 'Kinsco', 'KONVIO', 'JX PERT', 
             'FLOJET', 'Eureka Forbes Aquasure from Aquaguard', 'Water Solution', 'SAMTA', 'RUIQUAN', 
             'Perfect Zone', 'Peore', 'Maxpure', 'Home-pro', 'Hi Tech', 
             'Ojhashree', 'Skyguard', 'FABER', 'Alkalinelife', 'CUCKOO', 
             'Aquatec Plus', 'Aqua Supreme', 'Antbell', 'Proven', 'Unicorn', 
             'Quantech', 'PureMyst', 'Prodrop', 'Prestige', 'PUREJAL', 
             'EUREKA FORBES', 'DPW', 'Aqua Libra', 'Aquaforte', 'Prisaa', 
             'HIMAJAL', 'Feelpure', 'FESCHON',       
               ],      
        "searchKey":"Water purifier",
        "getRow": lambda row: giveMeProductRow('WATER PURIFIER',row)
    },
]