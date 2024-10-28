import json
import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

ficheroUsers =  'api/ficheros/users.json'

usersBP = Blueprint('users',__name__)

def leerFichero(fichero):
    archivo = open(fichero, 'r')
    users = json.load(archivo)
    archivo.close()
    return users

def escribirFichero(programadores):
    archivo = open('api/ficheros/users.json', 'w')
    json.dump(programadores, archivo)
    archivo.close()

#POST
@usersBP.post("/")
def addUser():
    users = leerFichero(ficheroUsers)
    if request.is_json:
        user = request.get_json()
        password = user["password"].encode("utf-8")
        salt = bcrypt.gensalt()
        hashPassword = bcrypt.hashpw(password,salt).hex()
        user["password"] = hashPassword
        users.append(user)
        escribirFichero(users)
        token=create_access_token(identity=user["username"])
        return {"token":token},201
    return {"error": "Request must be JSON"},415

#GET
@usersBP.get("/")
def getUsers():
    return jsonify(leerFichero(ficheroUsers))