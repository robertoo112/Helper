
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
import os

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


# apt-get update && apt-get -y install python
# pip install flask pymongo Flask-PyMongo
# python /opt/source-code/


# FROM trow.kube-public:31000/ubuntu
# ADD ./gitrepo /opt/source_code/
# RUN apt-get update && apt-get -y install python && apt-get install -y python3-pip python-dev
# RUN pip install flask pymongo Flask-PyMongo
# CMD python /opt/source-code/gitrepo/app2.py


# FROM ubuntu:18.04
# ADD ./gitrepo /app
# RUN apt-get update && apt-get -y install python && apt-get -y install python3-pip python-dev
# WORKDIR /app
# RUN pip3 install -r requirements.txt
# CMD python3 /app/app2.py

servicio_db = os.getenv('HOSTNAME')
password_db = os.getenv('PASSWORD')
user_db = os.getenv('USERNAME')
port_db = os.getenv('PORT')
if servicio_db == None:
    servicio_db = "mongo-svc"
if password_db == None:
    password_db = "admin"
if user_db == None:
    user_db = "admin"
if port_db == None:
    port_db = 27017
MONGO_URI = "mongodb://"+user_db+":"+password_db+"@"+servicio_db+":"+port_db+"/pythonmongodb"



app.secret_key = 'myawesomesecretkey'

app.config['MONGO_URI'] = MONGO_URI

mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def create_user():
    # Receiving Data
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if username and email and password:
        hashed_password = generate_password_hash(password)
        #id = mongo.db.users.insert_one(
        #    {'username': username, 'email': email, 'password': hashed_password})
        response = jsonify({
            '_id': str(1000032),
            'username': username,
            'password': password,
            'email': email
        })
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response


@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if username and email and password and _id:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'username': username, 'email': email, 'password': hashed_password}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 8080, debug = True)
    mongo.db.hola.insert({'prueba1':'completada'})