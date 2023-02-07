from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://admin_chill:admin_chill777@cluster0.gof0p5r.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.sool


@app.route('/')
def home():
    return render_template('index.html')



@app.route("/finding", methods=["GET"])
def finding_get():
    x = request.args.get("alinfo","", type=str)
    finding_list = list(db.collect2.find({'productName':{'$regex':x}},{'_id': False}))
    return jsonify({'finding_box': finding_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)
