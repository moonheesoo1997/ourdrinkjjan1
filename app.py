from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.1zag6b7.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.ourdrinkjjan


@app.route('/')
def home():
    return render_template('index.html')



@app.route("/finding", methods=["GET"])
def finding_get():
    x = request.args.get("finding","",type=str)
    finding_list = list(db.search_box.find({'productName':{'$regex':x}}, {'_id': False}))
    return jsonify({'finding_box': finding_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
