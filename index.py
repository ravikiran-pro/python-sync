import threading
from flask import Flask,jsonify
from scrapper import scrapProduct

app = Flask(__name__)

@app.route("/sync")
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
