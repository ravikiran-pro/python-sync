import requests
import threading
from bs4 import BeautifulSoup
from utils import productData
from insertData import insertProduct

data=[]
base_url="https://www.flipkart.com"

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

def getDataFromProductLink(link,massage):
    try:    
        product={} 
        product["product_link"]=base_url+link['href']
        product_page=requests.get(base_url+link['href'])
        product_soup=BeautifulSoup(product_page.content,"html.parser")
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
        print(f"Inserting the scraped Data: {product['model_name']}")
        threading.Thread(target=insertProduct,args=(massage(product),)).start()

    except Exception as e:
        print(f"Error getDataFromProductLink: {str(e)}")
        print(f"link: {link}")
        threading.Thread(target=getDataFromProductLink,args=(link,massage)).start()

def productDetails(url,massage):
    try: 
        print(f"Scraping the page: {url}")
        main_page=requests.get(url)
        main_soup = BeautifulSoup(main_page.content, "html.parser")  
        product_links=[]
        class1=main_soup.find_all("a",class_="_1fQZEK",href=True)
        class2=main_soup.find_all("a",class_="s1Q9rs",href=True)
        class3=main_soup.find_all("a",class_="_2UzuFa",href=True)
        if(class1):
            product_links = class1
        elif(class2):
            product_links=class2 
        elif(class3):
            product_links=class3  
        for link in product_links:  
            threading.Thread(target=getDataFromProductLink,args=(link,massage)).start()
            # break
        next_page=main_soup.find_all("a",class_="_1LKTO3",href=True)
        if(next_page): 
                next_link=""
                if(len(next_page)==2):
                    if(next_page[1].text == "Next"):
                        next_link=next_page[1]["href"]
                else: 
                    if(next_page[0].text == "Next"):
                        next_link=next_page[0]["href"] 
                if(next_link):
                    next_link=base_url+next_link
                    productDetails(next_link, massage)

    except Exception as e:
        print(f"Error productDetails: {str(e)}")
        print(f"url: {str(url)}")
        print(f"massage: {str(massage)}")
        # productDetails(url,massage)

def scrapProduct():
    for product in productData:
        for value in product['brands']:
            q="all+"+value+"+"+ product['searchKey'] +"&augment=false"
            url = base_url+"/search?q="+str(q)
            print(f"Scraping thread of : {value} started")
            threading.Thread(target=productDetails,args=(url,product['getRow'])).start()

    print("All Threads started:")
    return {"message":"Product Data Synced!"}    
