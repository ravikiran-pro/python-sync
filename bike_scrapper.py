import json
import requests
import threading
import time
from bs4 import BeautifulSoup
from insertData import insertProduct
from urllib.parse import urlparse
from urllib.parse import parse_qs
from connection import client, products_collection
from multiprocessing import Process
from bson import ObjectId
from webdriver import ChromeHeadless
from datetime import datetime
import re


data=[]
base_url="https://www.91wheels.com/scooters"
headers = {}

thread_count = 0
max_thread_count = 25

current_datetime = datetime.now()
iso_string = current_datetime.isoformat()

def productDetails(brand, link, warranty_link , bike_type, coverage, alias):
    try: 
        main_page=requests.get(link, headers=headers)
        main_soup = BeautifulSoup(main_page.content, "html.parser")
        products = main_soup.find_all('div', class_="vehicle_card_style__CCardStyle-sc-1mqhyos-0 cWZEme radius-3 pos-r border")
        threads = []
        if len(products):
            for product in products:
                link = product.find('a')['href']
                name = product.find('a')['title']
                getDataFromProductLink(link, name, brand, warranty_link, bike_type, coverage, alias)
                # threads.append(threading.Thread(target=getDataFromProductLink, args=(link, name, brand, warranty_link, bike_type, coverage, alias)))
                # threads[-1].start()   
            # for thread in threads:
            #     thread.join()
            print('{} --- {} -- completed {}'.format(brand, bike_type, len(products)))
        else:
            print('no product found --- {}'.format(brand))
        

    except Exception as e:
        print(f"Error productDetails: {str(e)}")



def getDataFromProductLink(link, name, brand, warranty_link, bike_type, coverage, alias, redirect = True):
    try:    
        color_data = []
        product_page = requests.get(link, headers= headers)
        prod_soup = BeautifulSoup(product_page.content, "html.parser")
        variants = prod_soup.find_all('tr', class_="table_style__CTr-sc-1qo50z6-2 kIirDc")

        variants_listing = [{
            'link': link,
            "title": name
        }]
        if len(variants):
            for variant in variants:
                atag = variant.find('a')
                variants_listing.append({
                    'link': atag['href'],
                    "title": atag['title']
                })

        # specification    
            product_page = requests.get(link+'/specifications', headers= headers)
            prod_soup = BeautifulSoup(product_page.content, "html.parser")
            prod_soup.find_all('tbody', class_ = "table_style__CTbody-sc-1qo50z6-4 fDhzGn")[0]
            product_img = prod_soup.find('img')
            transmission_type = None
            engine_capacity = None
            fuel_capacity = None
            for tr in prod_soup.find_all('tr', class_="table_style__CTr-sc-1qo50z6-2"):
                if(tr.find('td')):
                    if tr.find('td').text == "Engine Capacity":
                        engine_capacity = tr.find_all('td')[1].text
                    if tr.find('td').text == "Type":
                        transmission_type = tr.find_all('td')[1].text
                    if tr.find('td').text == "Fuel Tank Capacity":	
                        fuel_capacity = tr.find_all('td')[1].text
            
        # colors
            product_page = requests.get(link+'/colours', headers= headers)
            prod_soup = BeautifulSoup(product_page.content, "html.parser")
            colours = prod_soup.find_all('span', class_="image_carousal_style__CCarouselCaption-sc-16ak642-2 cUEhhl")
            color_data = [colour.get_text() for colour in colours]
            model = link.split('/')[-1]
        

        for variant in variants_listing:
            link = variant['link']
            sub = link.split('/')[-1]

            modelNo = model if model == sub else model+'-'+sub
            
            filter = {"model_no": modelNo}
            isExist = products_collection.find_one(filter)
            if isExist is not None:
                print(f"Product Already Exists: Model : {modelNo}")
                continue

            for color in color_data:
                data = {
                    'name': variant['title'] + ' ({}) '.format(color),
                    'product_type_id': '61645a921082c438b19ad833',
                    'category_id': '61645a921082c438b19ad82f',
                    'model': modelNo,
                    'model_no': modelNo,
                    'brand': brand,
                    'product_link': link,
                    'img': product_img['src'],
                    'PID': "",
                    "brand_image": "https://images.91wheels.com/images/brand-logos/bikes/{}.jpg?w=100&q=60".format(alias),
                    "specifications": {
                        'engine_capactiy': engine_capacity,
                        'transmission_type': transmission_type,
                        'fuel_type': 'petrol' if fuel_capacity != None else 'electric',
                        'type': bike_type,
                        'color': color
                    },
                    'color': color,
                    "warranty_details": {
                    "warranty_summary": coverage,
                    "link": warranty_link
                    },
                    'is_active': True,
                    'created_at': iso_string,
                    'updated_at': iso_string,
                }
                insertProduct(data)
        
    except Exception as e:
        print(f"Error getDataFromProductLink: {str(e)}")
        if redirect:
            time.sleep(30)
            getDataFromProductLink(link, name, brand, warranty_link, bike_type, coverage, False)     


def scrapBikes():    
    bikes = [
        {
            "name": "Royal Enfield",
            "type": ["bike"],
            "coverage": ["5 years or 75000 Km"]
        },
        {
            "name": "TVS",
            "wl": "https://www.tvsmotor.com/customers/warranty-policy",
            "type": ["scooter", "bike"],
            "coverage": ["5 years or 50000 Km", "5 years or 75000 Km"]
        },
        {
            "name": "Bajaj",
            "wl": "https://kaydeeauto.in/warranty-on-bajaj-bike/#:~:text=following%20terms%20%26%20conditions.-,TERMS%20%26%20CONDITIONS,from%20the%20date%20of%20purchase.",
            "type": ["scooter", "bike"],
            "coverage": ["5 years or 75000 Km", "5 years or 75000 Km"]
        },
        {
            "name": "Hero",
            "alias": "heromotocorp",
            "type": ["scooter", "bike"]
        },
        {
            "name": "kawasaki",
            "type": ["bike"],
            "wl": "https://kawasaki-india.com/wp-content/uploads/2022/07/k-care-brochure-2.pdf",
            "coverage": ["2 years or 30000 Km"]
        },
        {
            "name": "Komaki",
            "type": ["scooter"]
        },
        {
            "name": "Honda",
            "wl": "https://www.honda2wheelersindia.com/services/honda-shield",
            "type": ["scooter", "bike"],
            "coverage": ["3 years or 36000 Km", "3 years or 42000 Km"]
        },
        {
            "name": "Suzuki",
            "wl": "https://www.suzukimotorcycle.co.in/best-value/warranty",
            "type": ["scooter", "bike"],
            "coverage": ["1 year or 12000 Km"]
        },
        {
            "name": "Lectrix",
            "type": ["scooter"]
        },
        {
            "name": "JAWA",
            "type": ["bike"]
        },
        {
            "name": "Yamaha",
            "type": ["scooter", "bike"]
        },
        {
            "name": "KTM",
            "wl": "https://www.ktm.com/en-in/service/warranty.html",
            "type": ["scooter", "bike"],
            "coverage": ["24 months manufacture warranty"]
        },
        {
            "name": "Yezdi",
            "type": ["bike"]
        },
        {
            "name": "Aprilia",
            "type": ["scooter", "bike"],
            "coverage": ["24 months"]  

        },
        {
            "name": "BMW",
            "wl": "https://www.bmw-motorrad.in/en/service/services/warranty.html",
            "type": ["bike"],
            "coverage": ["3 years"]  
        },
        {
            "name": "Ducati",
            "wl": "https://www.ducati.com/ww/en/service-maintenance/ducati-warranty#:~:text=Ducati%20covers%20every%20bike%20for,after%20registration%20with%20unlimited%20mileage.&text=Throughout%20the%20world%2C%20Ducati%20offers,team%20of%20passionate%2C%20expert%20technicians.",
            "type": ["bike"],
            "coverage": ["24 months"]  
        },
        {
            "name": "Harley-Davidson",
            "wl": "https://www.harley-davidson.com/in/en/customer-service/warranty.html",
            "alias": "harleydavidson",
            "type": ["bike"]
        },
        {
            "name": "Hero Electric",
            "type": ["scooter", "bike"]
        },
        {
            "name": "Ola Electric",
            "alias": 'ola-electric',
            "type": ["scooter", "bike"]
        },
        {
            "name": "Revolt Motors",
            "wl": "https://www.revoltmotors.com/charging",
            "type": ["bike"],
            "coverage": ["3 years or 40,000 kilometers"]  
        },
        {
            "name": "Ampere",
            "type": ["scooter"]
        },
        {
            "name": "Ather",
            "wl": "https://assets.atherenergy.com/warranty_policy.pdf?_gl=1*17a89l3*_ga*NDk5MDkzMTg4LjE3MDA3MzYwMDU.*_ga_F6PH8BR8G8*MTcwMTE1NjM1NC4yLjEuMTcwMTE1NjQwMC4xNC4wLjA.",
            "type": ["scooter"],
            "coverage": ["3 years or 30000 Km"]
        },
        {
            "name": "Vespa",
            "wl": "https://www.vespa.com/us_EN/aftersales/",
            "type": ["scooter"],
            "coverage": ["24 months"]
        }
    ]
    brands_list = []

    for bike in bikes:
        name = bike['name']
        alias = bike.get('alias', name.lower().replace(" ",""))
        warranty_link = bike.get('wl', None)
        coverage = bike.get('coverage', [None])
        if(len(bike['type']) == 2):
            brands_list.extend([
                {
                    'name': name,
                    'link': 'https://www.91wheels.com/bikes/{}'.format(alias),
                    'warranty_link': warranty_link,
                    "type": 'bike',
                    "coverage": coverage[1] if coverage and len(coverage) > 1 else coverage[0]
                },
                {
                    'name': name,
                    'link': 'https://www.91wheels.com/scooters/{}'.format(alias),
                    'warranty_link': warranty_link,
                    "type": 'scooter',
                    "coverage": coverage[0] if coverage else None
                }
            ])
        else:
            brands_list.append({
                'name': name,
                'link': 'https://www.91wheels.com/{}s/{}'.format(bike['type'][0], alias),
                'warranty_link': warranty_link,
                "type": bike['type'][0],
                "coverage": coverage[0] if coverage else None
            })
    threads = []
    for list in brands_list:
        productDetails(list['name'], list['link'], list['warranty_link'], list['type'], list['coverage'], alias)
        # threads.append(threading.Thread(target=productDetails, args=(list['name'], list['link'], list['warranty_link'], list['type'], list['coverage'], alias)))
        # threads[-1].start()
    
    # for thread in threads:
    #     thread.join()


    print("All Threads started:")
    client.Close()
    return {"message":"Product Data Synced!"}    
