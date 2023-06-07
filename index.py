from flask import Flask
from scrapper import scrapProduct

app = Flask(__name__)

@app.route("/sync")
def hello_world():
    return scrapProduct()

@app.route("/")
def health():
    return {
        "message": "Server is running...."
    }
    