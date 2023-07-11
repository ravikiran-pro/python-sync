import threading
from flask import Flask,jsonify
from scrapper import scrapProduct
from connection import Mongo
app = Flask(__name__)

@app.route("/sync", methods= ['POST'])
def hello_world():
    threading.Thread(target=scrapProduct).start()
    return jsonify({
        "message": "Product Data Sync Started!"
    })
@app.route("/")
def health():
    return {
        "message": "Server is running...."
    }
    
app.config['DEBUG'] = True
