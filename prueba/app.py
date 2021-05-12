from pymongo import MongoClient
import os

servicio_db = os.environ['HOSTNAME']
password_db = os.environ['PASSWORD']
user_db = os.environ['USERNAME']
MONGO_URI = "mongodb://"+user_db+":"+password_db+"@"+servicio_db

client = MongoClient(MONGO_URI)

db = client['prueba']
collection = db['coleccion']

collection.inssert_one({"name":"prueba1", "resultado": "funciona!"})