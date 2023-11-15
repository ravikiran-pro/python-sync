import json
import requests
import threading
import time
from bs4 import BeautifulSoup
from utils import productData
from insertData import insertProduct
from urllib.parse import urlparse
from urllib.parse import parse_qs
from connection import client, products_collection
from multiprocessing import Process
from bson import ObjectId
import re


data=[]
base_url="https://www.flipkart.com"
thread_count = 0
max_thread_count = 25

def getText(element):
    if(element):
       return element.text.strip()
    else:
        return ""

def getTableData(element):
    data_dict = {}
    for row in element.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 0: 
            key = cells[0].text.strip()
            if(key and len(cells) > 1):
                value = cells[1].text.strip()
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
        parsed_url = urlparse(base_url+link)
        product['url'] = base_url+link
        product['pid'] = parse_qs(parsed_url.query)['pid'][0]
        filter = {'PID': product['pid']}
        isExist = products_collection.find_one(filter)
        if isExist is not None:
            print(f"Product Already Exists: PID : {product['pid']}")
            return 

        product['brand_name'] = value
        # product_page=requests.get(base_url+link) // Not working for the category Juicer,mixer & grinder
        product_page=requests.post(base_url+link)
        product_soup=BeautifulSoup(product_page.content,"html.parser")

        
        if type=='PRINTER':
            a_element = product_soup.find('div', class_='_3GIHBu').find('a', class_='_2whKao')

            if a_element:
                if ("Printers"!= a_element.text):
                    print("--Skip other then Printer-----",a_element.text)
                    return
                elif a_element is None:
                    print("--Skip if category is None-----",a_element)
                    return
                
        elif type=='SMART WATCH':
            a_element = product_soup.find('a', class_='_2whKao', text='Smart Watches')

            if a_element:
                if ("Smart Watches"!= a_element.text):
                    print("--Skip other then Smart Watches-----",a_element.text)
                    return
            elif a_element is None:
                 print("--Skip if category is None-----",a_element)
                 return
            
        elif type=='JUICER, MIXERS & GRINDERS':
            a_element = product_soup.find('a', class_='_2whKao', text='Mixer Juicer Grinder')
            

        product_images=product_soup.find_all("img",class_="q6DClP",src=True)
        brand_image_div=product_soup.find_all("div",class_="_3nWYNs")
        brand_image=''
        if len(brand_image_div):
            brand_image= brand_image_div[0].find_all("img")[0]['src']
        model_name=getText(product_soup.find("span",class_="B_NuCI"))
        description=getText(product_soup.find("div",class_="_1mXcCf RmoJUa"))
        img=[image['src'] for image in product_images] 
        rating=getText(product_soup.find("div",class_="_3LWZlK"))
        review=getText(product_soup.find("span",class_="_2_R_DZ")) 
        original_price=getText(product_soup.find("div",class_="_3I9_wc _2p6lqe"))
        discount_price=getText(product_soup.find("div",class_="_30jeq3 _16Jk6d"))
        discount_percent=getText(product_soup.find("div",class_="_3Ay6Sb _31Dcoz"))
        if not original_price:
            original_price=discount_price
        storage=[]
        color=[]
        ram=[]
        size=[]
        washing_capacity=[]
        wifi_connectivity=[]
        li_tooltip=product_soup.find_all("li",class_="_3V2wfe")
        for tool in li_tooltip:
            id=tool["id"]  
            if "storage" in id and tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM"):
                storage.append(tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM").text)
            if "ram" in id and tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM"):
                ram.append(tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM").text)
            if "color" in id and tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM"):
                color.append(tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM").text)
            if "size" in id and tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM"):
                size.append(tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM").text)
            if "washing_capacity" in id and tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM"):
                washing_capacity.append(tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM").text)
            if "wifi_connectivity" in id and tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM"): 
                wifi_connectivity.append(tool.find("div",class_="_2OTVHf _3NVE7n _1mQK5h _2J-DXM").text)
        highlights_element=product_soup.find_all("li",class_="_21Ahn-")
        highlights=[h.text.strip() for h in highlights_element] 
        table_elements=product_soup.findAll("table",class_="_14cfVK")
        specs={}
        details=getGridData(product_soup)
        watt = None
        for text in highlights:
            match = re.search(r'(\d+(?:\s*W)?)\s*:\s*Higher the Wattage', text)
            if match:
                watt_value = match.group(1)
                watt = watt_value
                # print(watt)
                break
        if(table_elements):
            for table in table_elements:
                specs.update(getTableData(table))
        product["images"]=(img) 
        product["brand_image"]=brand_image 
        product["model_name"]=model_name
        product["description"]=description
        product["rating"]=rating
        product["review"]=review
        product["original_price"]=original_price
        product["discount_price"]=discount_price
        product["discount_percent"]=discount_percent
        product["storage"]=storage 
        product["color"]=color 
        product["ram"]=ram 
        product["size"]=size 
        product["washing_capacity"]=washing_capacity 
        product["wifi_connectivity"]=wifi_connectivity 
        product["highlights"]=highlights 
        product["specs"]=specs 
        product["details"]=details 
        product["Watt"] = watt

        print(f"Inserting the scraped Data: {product['model_name']}")
        insertProduct(massage(product))

    except Exception as e:
        print(f"Error getDataFromProductLink: {str(e)}")
        print(f"link: {link}")
        time.sleep(30)
        getDataFromProductLink(link, value, massage)

def productDetails(url, massage, callBack):
    next_link=""
    try: 
        main_page=requests.post(url)
        # main_page=requests.get(url) // Not working for the category Juicer,mixer & grinder
        main_soup = BeautifulSoup(main_page.content, "html.parser")
        product_links=[]
        class1=main_soup.find_all("a",class_="_1fQZEK",href=True)
        class2=main_soup.find_all("a",class_="s1Q9rs",href=True)
        class3=main_soup.find_all("a",class_="_2UzuFa",href=True)
        if(class1):
            product_links.append(class1)
        elif(class2):
            product_links.append(class2)
        elif(class3):
            product_links.append(class3)  
        
        callBack(product_links[0])
        
        next_page=main_soup.find_all("a",class_="_1LKTO3",href=True)
        if(next_page): 
                if(len(next_page)==2):
                    if(next_page[1].text == "Next"):
                        next_link=next_page[1]["href"]
                else: 
                    if(next_page[0].text == "Next"):
                        next_link=next_page[0]["href"] 
                if(next_link):
                    next_link=base_url+next_link
                    productDetails(next_link, massage, callBack)

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
        getDataFromProductLink(link['href'],type, value, massage)
    callBack()

def scrapBrandDetails(brands,type, searchKey, getRow):
    threads = []
    for value in brands:
        if type=='SMART WATCH':
            
             q="all+"+value+"+"+ searchKey +"&as-show=on&as=off&augment=false&p%5B%5D=facets.brand%255B%255D%3D"+value
             url = base_url+"/search?q="+str(q)

        if type == 'JUICER, MIXERS & GRINDERS':
            q="all+"+value+"+"+ searchKey +"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&augment=false"
            url = base_url+"/search?q="+str(q)

        else:        
            q="all+"+value+"+"+ searchKey +"&as-show=on&as=off&augment=false"
            url = base_url+"/search?q="+str(q)
            
        print(f"Scraping thread of : {value} started \n base url: ${url}")
        baseThread = BaseThread(
                target=productDetails, 
                type=type,
                url = url, 
                value = value,
                getRow = getRow
            )
        # threads.append(baseThread.start())
        baseThread.start()
    #     threads[-1].start()
    # for t in threads:                                                           
    #     t.join() 

def scrapProduct():
    for product in productData:
        if product['type'] == 'JUICER, MIXERS & GRINDERS':
            scrapBrandDetails(product['brands'],product['type'] , product['searchKey'], product['getRow'])
        # if product['type'] == 'PRINTER':
        #     scrapBrandDetails(product['brands'],product['type'] , product['searchKey'], product['getRow'])
        # elif product["type"] == 'SMART WATCH':
        #     scrapBrandDetails(product['brands'],product['type'] , product['searchKey'], product['getRow'])
    print("All Threads started:")
    client.Close()
    return {"message":"Product Data Synced!"}    
