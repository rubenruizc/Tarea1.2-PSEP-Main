from flask import *
from flask_jwt_extended import JWTManager
from api.personas.personas import personasBP
from api.moviles.moviles import movilesBP
from api.users.routes import usersBP

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AMARU'
jwt = JWTManager(app)

app.register_blueprint(personasBP,url_prefix='/personas')
app.register_blueprint(movilesBP,url_prefix='/moviles')
app.register_blueprint(usersBP,url_prefix='/users')