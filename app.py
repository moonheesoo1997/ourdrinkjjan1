from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
app.config['JSON_AS_ASCII'] = False

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.qayzulj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

product_db = client.ourdrinkjjan

@app.route('/')
def home():
   return render_template('detail.html')

@app.route("/detail", methods=["POST"])
def detail_post():

    product_id_receive = request.form["product_id"]
    name_receive = request.form["name_give"]
    comment_receive = request.form["comment_give"]

    doc = {
        'name': name_receive,
        'comment': comment_receive,
        'Productid': int(product_id_receive)
    }

    product_db.comments.insert_one(doc)
    return jsonify({'msg':'댓글이 등록되었습니다.'})


@app.route("/detail/<product_id>", methods=["GET"])
def productid_get(product_id):
    print("prod_id: " + product_id)

    sool = product_db.search_box.find_one({'Productid' : int(product_id)})
    data = dict(sool)
    return render_template('detail.html',
                           Productid = data['Productid'],
                           Productname = data['productName'],
                           imageLink = data['imageLink'],
                           alcohol = data['alcohol'],
                           capacity = data['capacity'],
                           intro = data['intro'],
                           type = data['type']
                            # text=data['text'],
                           # scent=data['scent']
                           )


@app.route("/detail/<product_id>/comments", methods=["GET"])
def commets_get(product_id):

    comment_list = list(product_db.comments.find({'Productid' : int(product_id)}, {'_id': False}))
    return jsonify({'comments':comment_list})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)