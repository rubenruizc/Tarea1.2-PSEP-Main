from flask import *

from api.personas.personas import personasBP

app = Flask(__name__)

movilesBP = Blueprint('moviles', __name__)

personasFichero = "api/ficheros/personas.json"
movilesFichero = "api/ficheros/moviles.json"

def leerFichero(fichero):
    archivo = open(fichero, 'r')
    moviles = json.load(archivo)
    archivo.close()
    return moviles

def escribirFichero(personas):
    archivo = open('api/ficheros/moviles.json', 'w')
    json.dump(personas, archivo)
    archivo.close()

# GET
@movilesBP.get("/")
def getMoviles():
    return jsonify(leerFichero(movilesFichero))

def findPersona(id):
    personas = leerFichero(personasFichero)

    for persona in personas:
        if persona['Id'] == id:
            return persona
    return ""

@movilesBP.get("/<int:id>/personas")
def getPersonaByMovil(id):
    moviles = leerFichero(movilesFichero)
    for movil in moviles:
        if movil['Id'] == id:
            list = findPersona(movil['IdPersona'])
            if len(list) > 0:
                return list, 200
            else:
                return {'error': 'No se ha encontrado ninguna persona para este móvil'}
    return {'error': 'Ese móvil no existe'}, 404



@movilesBP.get("/<int:id>")
def getMovilById(id):
    moviles = leerFichero(movilesFichero)
    for movil in moviles:
        if movil['Id'] == id:
            return movil, 200
    return {"error": "No existe un móvil con dicho ID"}, 404

# PUT
def findNextId():
    moviles = leerFichero(movilesFichero)
    return max(movil["Id"] for movil in moviles) + 1

@movilesBP.post("/")
def addMovil():
    if request.is_json:
        movil = request.get_json()

        movil["Id"] = findNextId()

        moviles = leerFichero(movilesFichero)
        moviles.append(movil)

        escribirFichero(moviles)
        return movil, 201

    return {"error", "Request must be json"}, 415

# PATCH
@movilesBP.put("/<int:id>")
@movilesBP.patch("/<int:id>")
def updateMovil(id):
    if request.is_json:
        newMovil = request.get_json()

        moviles = leerFichero(movilesFichero)
        for movil in moviles:
            if movil['Id'] == id:
                for element in newMovil:
                    movil[element] = newMovil[element]
                escribirFichero(moviles)
                return movil, 200

    return {"error": "Request must be a JSON"}, 415

@movilesBP.delete("/<int:id>")
def deleteMovil(id):
    moviles = leerFichero(movilesFichero)
    for movil in moviles:
        if movil["Id"] == id:
            moviles.remove(movil)

            escribirFichero(moviles)
            return "{}", 200
    return {"error": "No se encuentra ningún móvil con ese ID"}, 404