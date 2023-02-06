from flask import Flask, render_template, request, jsonify

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
    print(request.args.get('test'))
    request.args.get("alinfo", type=str)
    finding_list = list(db.search_box.find({'productName':{'$regex':x}},{'_id': False}))
    return jsonify({'finding_box': finding_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)
