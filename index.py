import threading
from flask import Flask,jsonify
from scrapper import scrapProduct
from connection import Mongo
from get_brands import getBrandsDetails
from get_specs_data import updateSpecsData
from bike_scrapper import scrapBikes
from car_scrapping import scrapCar
import json

app = Flask(__name__)

@app.route("/sync", methods= ['POST'])
def scrap():
    threading.Thread(target=scrapProduct).start()
    return jsonify({
        "message": "Product Data Sync Started!"
    })

@app.route("/sync/91wheels", methods= ['POST'])
def scrap_bike():
    threading.Thread(target=scrapBikes).start()
    return jsonify({
        "message": "Product Data Sync Started!"
    })

@app.route("/sync/carEwala", methods= ['POST'])
def scrap_car():
    threading.Thread(target=scrapCar).start()
    return jsonify({
        "message": "Product Data Sync Started!"
    })

@app.route("/get_brands_details")
def get_brands_details():
    brand_details = getBrandsDetails()
    print(brand_details)
    d = json.dumps(brand_details)
    print(d)
    return jsonify(json.dumps(brand_details))
    

@app.route("/update_specs")
def update_specs():
    updateSpecsData()
    return {
        "message": "Server is running...."
    }

@app.route("/")
def health():
    return {
        "message": "Server is running...."
    }
    
app.config['DEBUG'] = True
