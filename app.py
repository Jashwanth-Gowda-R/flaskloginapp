from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "jashu"

app.config["MONGO_URI"] = "mongodb://localhost:27017/jashwanth"

mongo = PyMongo(app)


@app.route('/add', methods=['POST'])
def add_user():
    json = request.json
    name = json['name']
    email = json['email']
    password = json['password']

    if name and email and password and request.method == 'POST':
        hashed_password = generate_password_hash(password)
        id = mongo.db.jashwanth.insert({'name': name, 'email': email, 'password': hashed_password})

        resp = jsonify('user added successfully')
        resp.status_code = 200
        return resp

    else:
        return not_found()


@app.route('/users')
def users():
    user = mongo.db.jashwanth.find()
    resp = dumps(user)
    return resp


@app.route('/user/<id>')
def user(id):
    user = mongo.db.jashwanth.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route('/deleteuser/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.jashwanth.delete_one({'_id': ObjectId(id)})
    resp = jsonify("user deleted sucessfully ")
    resp.status_code = 200
    return resp


@app.route('/updateuser/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    json = request.json
    name = json['name']
    email = json['email']
    password = json['password']
    if name and email and password and _id and request.method == 'PUT':
        hashed_password = generate_password_hash(password)

        mongo.db.jashwanth.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                      {'$set': {'name': name, 'email': email, 'password': hashed_password}})

        resp = jsonify('user UPDATED successfully')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found' + ' ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == " __main__":
    app.run(debug=True)
