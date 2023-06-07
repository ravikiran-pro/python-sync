from flask import Flask
from scrapper import scrapProduct

app = Flask(__name__)

@app.route("/")
def hello_world():
    return scrapProduct()