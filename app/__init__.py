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


@app.route('/') #login
def home():
    return render_template("index.html")
 
@app.route('/home') #home
def inicio():
    return render_template("home.html")

#funciones del CRUD
@app.route('/crear')
def crear():
    return render_template("crear_receta.html")

@app.route('/editar')
def editar():
    return render_template("editar_receta.html")

@app.route('/ver')
def ver():
    return render_template("ver_receta.html")

@app.route('/eliminar')
def eliminar():
    return render_template("eliminar_receta.html")