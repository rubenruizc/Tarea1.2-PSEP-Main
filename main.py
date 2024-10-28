#coding: latin1
from time import sleep
import requests

from api.personas.personas import personasBP

username = input("User: ")
password = input("Password: ")
resultado = requests.post(
   "http://localhost:5050/users/login",
   json={"username": username, "password": password},
   headers={"Content-Type": "application/json"})
token = resultado.json().get("token")
print (token)


try:
   response = requests.get("http://localhost:5050/personas",headers={"Authorization": "Bearer " + token})
except Exception as e:
   print(e)

# Si la petición es exitosa
if response.status_code == 200:
   # Muestra el json correspondiente a la petición
   print(response.json())
# Si no, muestra este mensaje
else:
   print("Se ha producido un error")
sleep(2)	# Pausa la ejecución durante 2 segundos
