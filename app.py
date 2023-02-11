import random
import json
import requests
from pymongo import MongoClient
import certifi
from flask import Flask, render_template, jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from bson import ObjectId

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


app = Flask(__name__)
ca = certifi.where()
client = MongoClient('mongodb+srv://admin_chill:admin_chill777@cluster0.gof0p5r.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

db = client.sool

collection = db["sool"]


@app.route('/')
def home():
    return render_template('survey.html')


@app.route('/result')
def result():
    return render_template('result.html')


@app.route('/detail')
def detail():
    return render_template('detail.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/landing")
def landing():
    return render_template('survey.html')


@app.route("/survey", methods=["GET"])
def survey_result_get():
    response_type = request.args.get("type", type=str)
    survey_result_list = list(db.collect2.find({"type": response_type},
                                               {'_id': False}))
    sample_survey_result_list = random.sample(survey_result_list, 4)
    return jsonify({'collect2': sample_survey_result_list})


@app.route("/random", methods=["GET"])
def random_result_get():
    response_type = request.args.get("type", type=str)
    random_result_list = list(db.collect2.find({"type": {'$ne': response_type}},
                                               {'_id': False}))
    sample_random_result_list = random.sample(random_result_list, 4)
    return jsonify({'collect2': sample_random_result_list})


@app.route("/detail", methods=["POST"])
def detail_post():
    product_id_receive = request.form["product_id"]
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'Productid': product_id_receive
    }

    db.comments.insert_one(doc)
    return jsonify({'msg': '댓글이 등록되었습니다.'})


@app.route("/detail/<product_id>", methods=["GET"])
def productid_get(product_id):
    sool = db.collect2.find_one({'Productid': str(product_id)})
    data = dict(sool)
    return render_template('detail.html',
                           Productid=data['Productid'],
                           Productname=data['productName'],
                           imageLink=data['imageLink'],
                           alcohol=data['alcohol'],
                           capacity=data['capacity'],
                           intro=data['intro'],
                           type=data['type'],
                           text=data['text']
                           # scent = data['scent']
                           )


@app.route("/detail/<product_id>/comments", methods=["GET"])
def commets_get(product_id):
    comment_list = list(db.comments.find({'Productid': str(product_id)}, {'_id': False}))
    return jsonify({'comments': comment_list})


@app.route("/finding", methods=["GET"])
def finding_get():
    x = request.args.get("alinfo", type=str)
    finding_list = list(db.collect2.find({'productName': {'$regex': x}}, {'_id': False}))
    return jsonify({'finding_box': finding_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5003, debug=True)
