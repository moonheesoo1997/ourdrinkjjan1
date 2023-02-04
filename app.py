from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:ourdrinkjjan@cluster0.1zag6b7.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbourdrinkjjan


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/search", methods=["GET"])
def search_get():
    search_list = list(db.search_box.find({}, {'_id': False}))
    return jsonify({'search_box': search_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
