from json import JSONDecoder
from flask import *
import json

app = Flask(__name__)


personasFichero = "api/ficheros/personas.json"
movilesFichero = "api/ficheros/moviles.json"

personasBP = Blueprint('personas', __name__)

def leerFichero(fichero):
    archivo = open(fichero, 'r')
    personas = json.load(archivo)
    archivo.close()
    return personas

def escribirFichero(personas):
    archivo = open('api/ficheros/personas.json', 'w')
    json.dump(personas, archivo)
    archivo.close()

# GET
@personasBP.get("/")
def getPersonas():
    return jsonify(leerFichero(personasFichero))

@personasBP.get("/<int:id>/moviles")
def getMovilByPersona(id):
    personas = leerFichero(personasFichero)

    for persona in personas:
        if persona['Id'] == id:
            moviles = leerFichero(movilesFichero)
            list = []
            for movil in moviles:
                if movil['IdPersona'] == id:
                    list.append(movil)
            if len(list) > 0:
                return list, 200
            else:
                return {'error': 'No se ha encontrado ningún móvil asociado a esta persona'}
    return {'error': 'Esta persona no existe'}, 404

@personasBP.get("/<int:id>")
def getPersonaById(id):
    personas = leerFichero(personasFichero)
    for persona in personas:
        if persona['Id'] == id:
            return persona, 200
    return {"error": "No existe una persona con ese ID"}, 404

# PUT
def findNextId():
    personas = leerFichero(personasFichero)
    return max(persona["Id"] for persona in personas) + 1

@personasBP.post("/")
def addPersona():
    if request.is_json:
        persona = request.get_json()

        persona["Id"] = findNextId()

        personas = leerFichero(personasFichero)
        personas.append(persona)

        escribirFichero(personas)
        return persona, 201

    return {"error", "Request must be json"}, 415

# PATCH
@personasBP.put("/<int:id>")
@personasBP.patch("/<int:id>")
def updatePersona(id):
    if request.is_json:
        newPersona = request.get_json()

        personas = leerFichero(personasFichero)

        for persona in personas:
            if persona['Id'] == id:
                for element in newPersona:
                    persona[element] = newPersona[element]

                escribirFichero(personas)
                return persona, 200

    return {"error": "Request must be a JSON"}, 415

@personasBP.delete("/<int:id>")
def deletePersona(id):

    personas = leerFichero(personasFichero)

    for persona in personas:
        if persona["Id"] == id:
            personas.remove(persona)

            escribirFichero(personas)
            return "{}", 200
    return {"error": "No se encuentra ninguna persona con ese ID"}, 404
