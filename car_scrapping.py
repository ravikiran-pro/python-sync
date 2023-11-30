import json
import requests
import threading
import time
from bs4 import BeautifulSoup
from utils import giveMeSpecification,replace_all,iso_string
from insertData import insertProduct
from webdriver import ChromeHeadless
from urllib.parse import urlparse
from urllib.parse import parse_qs
from connection import client, products_collection
from multiprocessing import Process
from bson import ObjectId
import re


data=[]
base_url="https://www.carwale.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

thread_count = 0
max_thread_count = 25

def getText(element):
    if(element):
       return element.text.strip()
    else:
        return ""

def getTableData(element):
    data_dict = {}
    key = getText(element.find(class_="o-fHmpzP o-cpNAVm"))
    value = getText(element.find(class_= "o-eZTujG"))
    if key:
        data_dict[key] = value

    return data_dict

def getGridData(element): 
    details = {}
    rows = element.find_all("div",class_="row") 
    for row in rows:
        key = getText(row.find(class_="col col-3-12 _2H87wv"))
        if(key):
            value =getText(row.find(class_="col col-9-12 _2vZqPX"))
            details[key] = value
    details["description"]=getText(element.find("div",class_="_1AN87F"))
    return details

def getDataFromProductLink(link,type, value, massage):
    try:    
        product={} 
        parsed_url = base_url+link
        product_page = requests.get(parsed_url, headers= headers)
        prod_soup = BeautifulSoup(product_page.content, "html.parser")
        product_varients = []
        for varient in prod_soup.find_all('a', class_= "o-eZTujG o-jjpuv o-cVMLxW", href=True):
            link = varient.get('href')
            if link:
                product_varients.append(link)
        
        for link in product_varients:
            varient_url = base_url+link
            varient_page = requests.get(varient_url, headers= headers)
            product_soup = BeautifulSoup(varient_page.content, "html.parser")
            product['url'] = varient_url
            model_name=getText(product_soup.find("h1",class_="o-dOKno o-bNCMFw o-eqqVmt"))
            filter = {"specifications.Variant": model_name}
            isExist = products_collection.find_one(filter)
            if isExist is not None:
                print(f"Product Already Exists: Model : {model_name}")
                continue

            product['brand_name'] = value
            product_images=product_soup.find_all("div",class_="iyZWZe")
            brand_image=''
            if len(product_images):
                brand_image= product_images[0].find_all("img")[0]['src']

            description=getText(product_soup.find("div",class_="o-fzpilz o-bkmzIL o-cpNAVm o-fyWCgU vDnuC_"))
            img=""
            rating=getText(product_soup.find("p",class_="o-Hyyko o-fzoTsT o-eqqVmt o-cKuOoN o-lIIwF o-eZTujG"))
            review=getText(product_soup.find("span",class_="o-fzptZU o-KxopV o-cpNAVm")) 
            original_price=getText(product_soup.find("span",class_="o-Hyyko o-bPYcRG o-eqqVmt"))

            color_data = [] 
            # Define a regex pattern to match the colors
            pattern = r'colours:\s*([\w\s\(\),]+)'

            # varient_page = requests.get(varient_url, headers= headers)
            # product_soup.find_all('a', {'title': color_data[0]})[0].find('img')

            # Search for the pattern in the text
            match = re.search(pattern, description)

            # Check if the pattern is found
            if match:
                # Extract and process the colors
                colors_str = match.group(1).strip()
                all_colors = re.findall(r'\w[\w\s]*(?:\([\w\s,]+\))?', colors_str)

                # Split colors connected by "and"
                color_data = [color.strip() for sublist in [color.split(' and ') for color in all_colors] for color in sublist]

            spec_elements=product_soup.find_all('div', class_ = "o-dsiSgT o-eemiLE o-cYdrZi o-fzoTov o-fzoTzh o-cpnuEd")
            specs={}
            # details=getGridData(product_soup)
            if(spec_elements):
                for spec in spec_elements:
                    specs.update(getTableData(spec))

            for color in color_data:
                product["images"]=(img) 
                product["brand_image"]=brand_image 
                product["model_name"]=model_name + ' ' + color
                product["description"]=description
                product["rating"]=rating
                product["review"]=review
                product["original_price"]=original_price
                product["specs"]=specs 
                product["color"]=color


                print(f"Inserting the scraped Data: {product['model_name']}")
                insertProduct(massage(product))

    except Exception as e:
        print(f"Error getDataFromProductLink: {str(e)}")
        print(f"link: {link}")
        time.sleep(30)
        getDataFromProductLink(link, value, massage)

def massage_data(dataType,row):
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
        
    newRow['model_no'] =  newRow['model_no'][0] if len(newRow['model_no']) == 1 else newRow['model_no']
    newRow['model'] =  newRow['model_no'][0] if len(newRow['model_no']) == 1 else newRow['model']
    return newRow

def productDetails(url, massage, callBack):
    try: 
        main_page=requests.get(url, headers=headers)
        main_soup = BeautifulSoup(main_page.content, "html.parser")
        product_links=[]
        for class1 in main_soup.find_all("a",class_="o-brXWGL o-frwuxB",href=True):
            h_tag = class1.get('href')
            if h_tag:
                product_links.append(h_tag)
        for class2 in main_soup.find_all("a",class_="o-elzeOy o-bkmzIL CyctJJ",href=True):
            h_tag = class2.get('href')
            if h_tag:
                product_links.append(h_tag)
        
        callBack(product_links)

    except Exception as e:
        print(f"Error productDetails: {str(e)}")
        print(f"url: {str(url)}")
        print(f"massage: {str(massage)}")

class BaseThread():
    def __init__(self,type, target, url, value, getRow):
        self.url = url
        self.getRow = getRow
        self.brand_product_links = 0
        self.target = target
        self.value = value
        self.type=type

    def start(self):
        # return Process( target=self.target, args=(self.url, self.getRow, self.callBack))
        self.target(self.url, self.getRow, self.callBack)

    def callBack(self, product_links):
        self.brand_product_links += len(product_links)
        scrapProductLink(product_links,self.type, self.getRow, self.value, self.end)
        # process = Process(
        #     target= scrapProductLink,
        #     args= (product_links, self.getRow, self.value, self.end)
        # )
        # process.start()
        # process.join()

    def end(self):
        print(f"total products found in ${self.value}: {self.brand_product_links}")
        

def scrapProductLink(product_links,type, massage, value, callBack):
    for link in product_links:
        getDataFromProductLink(link,type, value, massage)
    callBack()

def scrapBrandDetails(brands,type, searchKey, getRow):
    threads = []
    for value in brands:
        if type == 'Car':
            # q="all+"+value+"+"+ searchKey
            url = base_url+ value["link"]

        else:        
            q="all+"+value+"+"+ searchKey +"&as-show=on&as=off&augment=false"
            url = base_url+"/search?q="+str(q)
            
        name = value["brand_name"]
        print(f"Scraping thread of : {name} started \n base url: ${url}")
        baseThread = BaseThread(
                target=productDetails, 
                type=type,
                url = url, 
                value = name,
                getRow = getRow
            )
        # threads.append(baseThread.start())
        baseThread.start()
    #     threads[-1].start()
    # for t in threads:                                                           
    #     t.join() 

def scrapCar():    
    main_page=requests.get(base_url, headers=headers)
    main_soup = BeautifulSoup(main_page.content, "html.parser")
    Brand_links = []
    for a_tag in main_soup.find_all('a', class_ = "o-cKuOoN o-frwuxB"):
        href_value = a_tag.get('href')
        brand_value = a_tag.get('title')
        if href_value:
            Brand_links.append({"link": href_value, "brand_name": brand_value})
    
    for product in productData:
        if product['type'] == 'Car':
            scrapBrandDetails(Brand_links,product['type'], product['searchKey'], product['getRow'])
    


    print("All Threads started:")
    client.Close()
    return {"message":"Product Data Synced!"}    

productData = [
    {
        "searchKey":"Car",
        "getRow": lambda row: massage_data('Car',row),
        "type": "Car"
    }
]