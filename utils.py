from datetime import datetime
from connection import brands
import json
import re


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
        'model': "",
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
        'product_link': row['url'],
        'img': row['images'][0] if row['images'] else 'https://prodkt-master.objectstore.e2enetworks.net/ProductPlaceholder.svg',
        'suggestion':"",
        'specifications': specifications,
        # 'brand_id': brands[row['brand_name']]['brand_id'],
        'PID': "",
        'is_active': True,
        'created_at': iso_string,
        'updated_at': iso_string,
        'scrap': json.dumps(row)
    }

    if dataType == 'Car':
        newRow['product_type_id'] = '61645a921082c438b19ae838'
        newRow['category_id'] = '61645a921082c438b19ad82f'
        newRow['brand'] = row['brand_name']
        newRow['model'] = row.get('model_name', {}).split(" (", 1)[0]
        if newRow['brand'] == "Maruti Suzuki":
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 Years/60,000 km",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://drive.google.com/file/d/1nVTllNFLbea0cPTC0kqpUCbZC-UfpKF6/view?usp=drive_link"
            }
        elif newRow['brand'] == 'Kia':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 Years / Unlimited Kms",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.kia.com/content/dam/kwcms/au/en/files/service/Kia-Warranty-terms-and-conditions.pdf"
            }
        elif newRow['brand'] == 'Toyota':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 Years / 100K Kms",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.toyotabharat.com/documents/extended-warranty/tw-tc.pdf"
            }
        elif newRow['brand'] == 'Honda':
            newRow['warranty_coverage'] = "3-Year"
            newRow['warranty_details'] = {
                'warranty_summary': "3-Year/36,000-Mile ",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.hondacarindia.com/honda-services/service-products/warranty"
            }
        elif newRow['brand'] == 'MG':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 Years/1 Lakh kms",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.mgmotor.co.in/service"
            }
        elif newRow['brand'] == 'Skoda':
            newRow['warranty_coverage'] = "4 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "4 years / 100,000 Kms",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.skoda-auto.co.in/other-offerings/4year-skoda-warranty"
            }
        elif newRow['brand'] == 'Jeep':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 Years / 100,000 km",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.jeep-india.com/content/dam/cross-regional/apac/jeep/en_in/app-icon/warranty-manual-compass.pdf"
            }
        elif newRow['brand'] == 'Nissan':
            newRow['warranty_coverage'] = ""
            newRow['warranty_details'] = {
                'warranty_summary': "",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': ""
            }
        elif newRow['brand'] == 'Renault':
            newRow['warranty_coverage'] = "2 Years"
            newRow['warranty_details'] = {
                'warranty_summary': " 2 years or 50,000 km",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.renault.co.in/terms-and-conditions.html"
            }
        elif newRow['brand'] == 'Volkswagen':
            newRow['warranty_coverage'] = "4 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "4 year (100,000 kilometers) ",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.volkswagen.co.in/en/owners/warranty.html"
            }
        elif newRow['brand'] == 'Citroen':
            newRow['warranty_coverage'] = "2 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "2 years/40,000 km",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://business.citroen.co.uk/maintain/citroen-warranty.html#:~:text=Every%20new%20Citro%C3%ABn%20enjoys%20the,your%20current%20warranty%20has%20expired."
            }
        elif newRow['brand'] == 'Audi':
            newRow['warranty_coverage'] = "5 Years"
            newRow['warranty_details'] = {
                'warranty_summary': " 5 years with unlimited mileage ",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.audi.in/in/web/en/customer-area/audi-owners/vehiclewarranty.html"
            }
        elif newRow['brand'] == 'Tata':
            models = {
                        "Indica/Indigo/Vista/Manza/Zest/Bolt/Tiago/Tigor/Nexon/Punch/Altroz/Safari 2.2 Dicor": "2 Years /75,000 Kms",
                        "Harrier": "2 Years /1,00,000 Kms",
                        "Nano": "4 Years /60,000 Kms",
                        "Aria/Storme/Sumo Gold/Grande/Movus/Hexa": "3 Years /1,00,000 Kms",
                        "Sumo Victa / Spacio ": "1.5 Years /Unlimited"
                    }
            for model, warranty_info in models.items():
                if any(substring.lower() in newRow['model'].lower() for substring in model.split('/')):
                    years_match = re.search(r'(\d+(\.\d+)?) Years', warranty_info)
                    newRow['warranty_coverage'] = years_match.group(1)
                    newRow['warranty_details'] = {
                        'warranty_summary': warranty_info,
                        'covered':row.get('specs',{}).get('Covered in Warranty',""),
                        'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                        'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                        'link': "https://cars.tatamotors.com/service/owners/information-on-warrant"
                    }
            else:
                newRow['warranty_coverage'] = ""
                newRow['warranty_details'] = {
                    'warranty_summary': "",
                    'covered':row.get('specs',{}).get('Covered in Warranty',""),
                    'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                    'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                    'link': ""
                }           
        elif newRow['brand'] == 'Hyundai':
            models = {
                        "Santro/NIOS/Aura/i20/N Line/Xcent/Grand i10": "3 Years / 100K Kms (Whichever is earlier) ",
                        "Venue/New Venue/Verna/Creta/Alcazar/Elantra/Tucson/Kona": "3 Years / Unlimited Kms ",
                    }
            for model, warranty_info in models.items():
                if any(substring.lower() in newRow['model'].lower() for substring in model.split('/')):
                    years_match = re.search(r'(\d+(\.\d+)?) Years', warranty_info)
                    newRow['warranty_coverage'] = years_match.group(1)
                    newRow['warranty_details'] = {
                        'warranty_summary': warranty_info,
                        'covered':row.get('specs',{}).get('Covered in Warranty',""),
                        'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                        'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                        'link': "https://www.hyundai.com/in/en/connect-to-service/warranty-policy/overview"
                    }
            else:
                newRow['warranty_coverage'] = ""
                newRow['warranty_details'] = {
                    'warranty_summary': "",
                    'covered':row.get('specs',{}).get('Covered in Warranty',""),
                    'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                    'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                    'link': ""
                }
        elif newRow['brand'] == 'Aston Martin':
            newRow['warranty_coverage'] = "2 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "2 years or 90,000 km",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.audiusa.com/us/web/en/service/warranty.html#:~:text=Audi%20warranties&text=The%20Audi%20New%20Vehicle%20Limited,Assistance%20at%20no%20additional%20cost.&text=The%20Audi%20Certified%20pre%2Downed,20%2C000%20miles%E2%80%94whichever%20occurs%20first."
            }
        elif newRow['brand'] == 'BMW':
            newRow['warranty_coverage'] = "2 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "2 years with unlimited mileage ",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.bmw.in/en/topics/owners/warranty-policy.html#:~:text=The%20entire%20vehicle%20(except%20for,from%20the%20warranty%20start%20date."
            }
        elif newRow['brand'] == 'BYD':
            newRow['warranty_coverage'] = "6 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "6 years/150,000 kilometer reading",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.byd.com/in/service/warranty-policy"
            }
        elif newRow['brand'] == 'Bentley':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 yr/10,000,000 km",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.bentleymotors.com/en/world-of-bentley/ownership/services/warranty.html"
            }
        elif newRow['brand'] == 'Jaguar':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 yr/100,000 km",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.jaguar.in/ownership/service-warranties/warranties/index.html#:~:text=For%20hassle%2Dfree%20repairs%20and,ever%20occurs%20earlier)%20manufacturer's%20warranty."
            }
        elif newRow['brand'] == 'Lamborghini':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3-years/unlimited mileage ",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.lamborghini.com/en-en/warranty-extension"
            }
        elif newRow['brand'] == 'Land Rover':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 yr/100,000 km",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.landrover.in/ownership/parts-warranty.html"
            }
        elif newRow['brand'] == 'Mercedes-Benz':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 years with unlimited mileage.",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.mercedes-benz.co.in/passengercars/services/warranty.html"
            }
        elif newRow['brand'] == 'Rolls-Royce':
            newRow['warranty_coverage'] = "4 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "four-year, unlimited mileage",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.rolls-roycemotorcars.com/chennai/en_GB/showroom.html?utm_source=google&utm_medium=cpc&utm_campaign=dealersearch&utm_content=july&gclid=Cj0KCQiA6vaqBhCbARIsACF9M6lRigItq1j9ou9xt35KhpTyPtX_NV33GKU6shYJo2lEChjZFCRFtHwaAgSlEALw_wcB"
            }
        elif newRow['brand'] == 'Volvo':
            newRow['warranty_coverage'] = "2 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "2 years with unlimited mileage.",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.volvocars.com/in/l/volvo-warranty/"
            }
        elif newRow['brand'] == 'Isuzu':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3-Year/50,000-Mile Basic Limited Warranty",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.isuzulv.com/warranty-information/"
            }
        elif newRow['brand'] == 'Bugatti':
            newRow['warranty_coverage'] = "4 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "four-year, unlimited mileage",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.bugatti.com/ownership/customer-service/#warranty"
            }
        elif newRow['brand'] == 'Porsche':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "The warranty (available for vehicles up to their 15th year* and with a mileage not exceeding 200,000 km/125.000 miles*) covers all components of your Porsche for 12, 24 or 36 months*",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.porsche.com/international/accessoriesandservice/porscheservice/vehicleinformation/approvedwarranty/"
            }
        elif newRow['brand'] == 'MINI':
            newRow['warranty_coverage'] = "2 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "two-year dealer warranty without mileage limitation",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.mini.in/en_IN/home/serv/service-and-repair/warranties.html"
            }
        elif newRow['brand'] == 'McLaren':
            newRow['warranty_coverage'] = "5 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "5 years or 45,000 miles",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.mclarenpalmbeach.com/mclaren-information/mclaren-warranty-coverage/#:~:text=McLaren%20New%20Vehicle%20Limited%20Warranty,%25%20State%20of%20Health%20(SoH)"
            }
        elif newRow['brand'] == 'Maserati':
            newRow['warranty_coverage'] = "4 Years"
            newRow['warranty_details'] = {
                'warranty_summary': " 4-year / 50,000-mile New Car Limited Warranty.",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.maseratili.com/manufacturer-information/what-does-a-maserati-warranty-cover/"
            }
        elif newRow['brand'] == 'Force Motors':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3 years / 3 Lac kms warranty with 7 free services.",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.forcegurkha.co.in/service/#warranty , https://www.forcemotors.com/Trax-DV.php"
            }
        elif newRow['brand'] == 'Ferrari':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "3-year/unlimited mileage factory warranty along with a seven-year free maintenance program.",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.ferrarifl.com/service/warranty/"
            }
        elif newRow['brand'] == 'Mahindra':
            newRow['warranty_coverage'] = ""
            newRow['warranty_details'] = {
                'warranty_summary': "",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': ""
            }
        elif newRow['brand'] == 'Lexus':
            newRow['warranty_coverage'] = "3 Years"
            newRow['warranty_details'] = {
                'warranty_summary': "three years or 1,00,000 km, whichever comes first. During this period, Lexus will repair or replace any defective Lexus-supplied part.",
                'covered':row.get('specs',{}).get('Covered in Warranty',""),
                'notCovered':row.get('specs',{}).get('Not Covered in Warranty',""),
                'serviceType':row.get('specs',{}).get('Warranty Service Type',""),
                'link': "https://www.lexusindia.co.in/en/servicing-and-support/warranty-coverage.html#"
            }
        

    if dataType == 'JUICER, MIXERS & GRINDERS':
        newRow['product_type_id'] = '654e01776a319ec3faebe641'
        newRow['category_id'] = '61645a921082c438b19ad831'
        newRow['brand'] = row['brand_name']
        if row['brand_name'] == 'Bajaj':
            brand = row['brand_name'].upper()
        elif row['brand_name'] == 'Wonderchef':
            brand = row['brand_name'].upper()
        else:
            brand = row['brand_name']
        match = re.search(rf'{re.escape(brand)}\s*(.*?)\s*(Mixer|Juicer)', row["model_name"])

        model = ''
        if match:
            model = match.group(1).strip()
        newRow['model']= model

    if dataType == 'MOBILE':
        if specifications.get('RAM','') == '' and specifications.get('Storage','') == '':
            return False
        newRow['brand']= row['model_name'].split(' ')[0].strip()
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Number',"")
        newRow['suggestion']= row['model_name'].split('(')[0].strip() + ' ' + specifications['RAM'].replace(' ', '').lower()+' '+specifications['Storage'].replace(' ', '').lower() +' '+specifications['Color'].lower()
        newRow['product_type_id'] = '61645a921082c438b19ad835'
        newRow['category_id'] = '61645a921082c438b19ad830'
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.RAM': specifications.get('RAM','NA'),
            'specifications.Color': specifications.get('Color','NA'),
            'specifications.Storage': specifications.get('Storage','NA'),
        }

    if dataType == 'AC':
        if specifications.get('Type') not in ['Window', 'Split']:
            return False
        newRow['brand']= row.get('specs', {}).get('Brand',"")
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= newRow['model'][newRow['model'].find("(")+1:newRow['model'].find(")")]
        newRow['suggestion']= row.get('specs', {}).get('Brand',"")+ ' ' + specifications["Type"]+' ac '+specifications["Capacity"].lower()
        newRow['product_type_id'] = '61645a921082c438b19ad844'
        newRow['category_id'] = '61645a921082c438b19ad831'
        newRow['filter'] = {
            'model_no': newRow.get('model',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Type': specifications.get('Type','NA'),
            'specifications.Inverter/Non-Inverter': specifications.get('Inverter/Non-Inverter','NA'),
            'specifications.Capacity': specifications.get('Capacity','NA'),
            'specifications.Rating': specifications.get('Rating','NA'),
        }
    
    if dataType == 'REFRIGERATOR':
        if specifications.get('Type','') == '' and specifications.get('Doors','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('model_name', {}).split(" L ")[0] + " L"
        newRow['model_no']= row.get('model_name', {}).split(",")[-1].strip()[:-1]
        newRow['warranty_coverage']= row.get('specs',{}).get('Warranty Summary',"").split('Warranty')[0].strip()
        newRow['suggestion']= newRow['brand'] + ' refrigerator ' + specifications["Capacity"].lower() + ' ' + specifications["Type"].lower() + ' ' + specifications["Rating"] + ' star'
        newRow['product_type_id'] = '61645a921082c438b19ad841'
        newRow['category_id'] = '61645a921082c438b19ad831'
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

    if dataType == 'TV':    
        if specifications.get('Type','') == '' and specifications.get('Size','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('model_name', {}).split(" (", 1)[0]
        newRow['model_no']= row.get('specs', {}).get('Model Name',"")
        newRow['product_type_id'] = '61645a921082c438b19ad845'
        newRow['category_id'] = '61645a921082c438b19ad831'
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

    if dataType == 'LAPTOP':    
        if specifications.get('Ram','') == '' and specifications.get('Processor','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',""),
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['product_type_id'] = '61645a921082c438b19ad836'
        newRow['category_id'] = '61645a921082c438b19ad830'
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
    
    if dataType == 'TABLET':    
        if specifications.get('RAM','') == '' and specifications.get('Storage','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['product_type_id'] = '61645a921082c438b19ad838'
        newRow['category_id'] = '61645a921082c438b19ad830'
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
    
    if dataType == 'WASHING MACHINE':    
        if specifications.get('Load','') == '' and specifications.get('Capacity','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Name',"")
        newRow['product_type_id'] = '61645a921082c438b19ad842'
        newRow['category_id'] = '61645a921082c438b19ad831'
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
    
    if dataType == 'PRINTER':    
        if specifications.get('Type','') == '':
            return False
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Name',"")
        newRow['product_type_id'] = '61645a921082c438b19ad83a'
        newRow['category_id'] = '61645a921082c438b19ad830'
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= newRow['brand'].split('(')[0].strip() + ' ' + specifications['Type'].replace(' ', '').lower()
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Type': specifications.get('Printing Method','NA'),
        }
    
    if dataType == 'CHIMNEY':  
        if specifications.get('Mount_type','') == '':
            return False  
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('model_name', {}).split('(')[1].split(')')[0]
        newRow['model_no']= row.get('specs', {}).get('Model Number',"").split(" (", 1)[0],
        newRow['product_type_id'] = '61645a921082c438b19ad846'
        newRow['category_id'] = '61645a921082c438b19ad831'
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
    
    if dataType == 'WATER PURIFIER': 
        if specifications.get('Capacity','') == '':
            return False     
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Name',"")
        newRow['product_type_id'] = '61645a921082c438b19ad847'
        newRow['category_id'] = '61645a921082c438b19ad831'
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

    if dataType == 'SMART WATCH':
        newRow['brand_id']=""
        newRow['brand']= row.get('model_name', {}).split(" ")[0]
        newRow['model']= row.get('specs', {}).get('Model Name',"")
        newRow['model_no']= row.get('specs', {}).get('Model Number',"")
        newRow['product_type_id'] = '61645a921082c438b19ad837'
        newRow['category_id'] = '61645a921082c438b19ad830'
        warranty_coverage = row.get('specs',{}).get('Warranty Summary',"")
        if (warranty_coverage):
            newRow['warranty_coverage'] = warranty_coverage.split('Warranty')[0].strip()
        newRow['suggestion']= newRow['name'].split('(')[0].strip() 
        newRow['filter'] = {
            'model_no': newRow.get('model_no',''),
            'model': newRow.get('model',''),
            'brand': newRow['brand'],
            'specifications.Color': specifications.get('Color','NA'),
        }
        
    newRow['model_no'] =  newRow['model_no'][0] if len(newRow['model_no']) == 1 else newRow['model_no']
    newRow['model'] =  newRow['model_no'][0] if len(newRow['model_no']) == 1 else newRow['model']
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


    if dataType == 'PRINTER':
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

    if dataType == 'SMART WATCH':
        return  {
            'Color': row.get('specs',{}).get('Strap Color','')
        }
    pass

    if dataType == "JUICER, MIXERS & GRINDERS":
        return {
            'Color': row['color'],
            'Watt': row['Watt']
        }
    pass

    if dataType == "Car":
        return {
            'Variant': row.get('model_name', ''),
            'Fuel Type': row.get('specs', {}).get('Fuel Type', ''),
            'Transmission': row.get('specs', {}).get('Transmission', ''),
            'Color': row.get('color', [])
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
        "getRow": lambda row: giveMeProductRow('MOBILE',row),
        "type": "MOBILE"
    },
    {
        "brands":[ 
            "Daikin","Voltas","Blue Star","LG","Hitachi","Carrier","Samsung","Whirlpool",
            "Godrej","Mitsubishi Electric","Panasonic","Lloyd","Haier","O General","Onida",
            "IFB","Sharp","TCL","Sanyo","Videocon"
        ],
        "searchKey":"ac",
        "getRow": lambda row: giveMeProductRow('AC',row),
        "type": "AC"
    },
    {
        "brands":[
            'LG', 'Samsung', 'Whirlpool', 'Haier', 'Godrej', 'Bosch', 'Panasonic', 'Voltas', 
            'Hitachi', 'IFB', 'Siemens', 'Kelvinator', 'Videocon', 'Onida', 'Toshiba', 'Electrolux', 
            'Sharp', 'Intex', 'Sansui', 'Mitashi', 'Blue Star', 'Croma', 'Lloyd', 'Kenstar'
        ],
        "searchKey":"refrigerator",
        "getRow": lambda row: giveMeProductRow('REFRIGERATOR',row),
        "type": "REFRIGERATOR"
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
        "getRow": lambda row: giveMeProductRow('TV',row),
        "type": "TV"
    },
    {
        "brands":[
            'Hp', 'Asus', 'Lenovo', 'Dell', 'Msi',
            'Apple', 'Avita', 'Acer', 'Samsung', 'Infinix',
            'Realme', 'Gigabyte', 'Vaio', 'Primebook', 'Alienware',
            'Smartron', 'Microsoft', 'Lg Gram',  
        ],
        "searchKey":"laptop",
        "getRow": lambda row: giveMeProductRow('LAPTOP',row),
        "type": "LAPTOP"
    },
    {
        "brands":[
            'Honor', 'Mi', 'OnePlus', 'Oppo', 'Apple',
            'Spigen', 'Samsung', 'Lenovo', 'Huawei', 'Asus',
            'Xiaomi', 'Dell', 'HP', 'Google', 'Tcl',
            'Alcatel', 'Iball', 'Honor', 'Motorola',
              ],
        "searchKey":"tablet",
        "getRow": lambda row: giveMeProductRow('TABLET',row),
        "type": "TABLET"
    },
    {
        "brands":[
             'Samsung', 'LG', 'Whirlpool', 'IFB', 'Panasonic', 
             'Motorola', 'Thomson', 'Godrej', 'Bosch', 'Voltas beko', 
             'Haier', 'Lloyd', 'Onida', 
              ],
        "searchKey":"washing machine",
        "getRow": lambda row: giveMeProductRow('WASHING MACHINE',row),
        "type": "WASHING MACHINE"
    },
    {
        "brands":[
             'HP','Canon','Epson','PANTUM','Brother','TVS ELECTRONICS','CPS',
            'Lenmark','KonicaMinolta','Samsung'
        ],
        "searchKey":"printers only",
        "getRow": lambda row: giveMeProductRow('PRINTER',row),
        "type": "PRINTER"
    },
    {
        "brands":[
             'Elica', 'Faber', 'Hindware', 'Glen', 'Sunflame',
             'Prestige', 'Kaff', 'Bosch', 'Inalsa', 'Kutchina', 
             'V-Guard',        
               ],
        "searchKey":"Chimney",
        "getRow": lambda row: giveMeProductRow('CHIMNEY',row),
        "type": "CHIMNEY"
    },
    {
        "brands": [
            "boAt", "Noise", "Amazfit", "Samsung", "CrossBeats", "Spigen", "Garmin", "beatXP",
            "Pebble", "TAGG", "HAMMER", "Fastrack", "ZEBRONICS", "GIZMORE", "Fitbit", "Apple",
            "Vibez", "Helix", "Maxima", "sekyo", "AJO", "Fitshot", "Casio", "Fire-Boltt", "Titan",
            "Fossil", "TIMEX","Sonata",  "Diesel",
            # "SKMEI",   "Chumbak", "Citizen","ADAMO", "Tommy Hilfiger", "LORENZ", "REDUX",
        ],
        "searchKey":"smart watch",
        "getRow": lambda row: giveMeProductRow('SMART WATCH',row),
        "type": "SMART WATCH"
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
        "getRow": lambda row: giveMeProductRow('WATER PURIFIER',row),
        "type": "WATER PURIFIER"
    },
    {
        "brands": [
            "Lifelong", "Prestige","PHILIPS", "Bajaj", "Wonderchef", "Bosch", "Butterfly", "Havells", "Preethi", "USHA", "Pigeon", "Morphy Richards", 
            "Sujata", "Vidiem", "Faber", "amazon basics", "Crompton", "BOROSIL", "Orient Electric", "Amirthaa", "Thomson", "Premier", "SOWBAGHYA", "Panasonic",
            "COOKWELL", "Maharaja Whiteline", "Inalsa", "PRINGLE", "BOSS",  "BAJAJ VACCO", "Swiss Military", "Lesco",
            "STARGAZE", "InstaCuppa", "Greenchef", "Veronica", "RIEO", "Kutchina", "FLORITA", "Ketvin", "SmartFingers",
            "MAYUMI", "Hamilton Beach", "KENT", "AGARO", "Rico", "SOLARA", "Ponmani"
        ],
        "searchKey":"Juicer, Mixers & grinders",
        "getRow": lambda row: giveMeProductRow('JUICER, MIXERS & GRINDERS',row),
        "type": "JUICER, MIXERS & GRINDERS"
    },
    {
        # "brands": [],
        "searchKey":"Car",
        "getRow": lambda row: giveMeProductRow('Car',row),
        "type": "Car"
    }
]