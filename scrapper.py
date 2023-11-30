import json
import requests
import threading
import time
from bs4 import BeautifulSoup
from utils import productData
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
            # isExist = products_collection.find_one(filter)
            # if isExist is not None:
            #     print(f"Product Already Exists: Model : {model_name}")
            #     continue

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

def scrapProduct():    
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
