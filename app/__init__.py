# archivo especial por eso los guines bajos
# especial para configurar flask, solo importar cosas para iniciar programa, define la carpeta como el cerebro del proyecto

from flask import Flask
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
CORS(app)

from app.routes import login
from app.routes import receta
from app.models import init_db, crear_usuario

init_db()
def crear_usuario_si_no_existe():
    try:
        crear_usuario("admin", "admin@gmail.com", "1234")
        print("Usuario admin creado")
    except Exception as e:
        print("Usuario admin ya existe o error:", e)

crear_usuario_si_no_existe()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/home')
def inicio():
    return render_template("home.html")



