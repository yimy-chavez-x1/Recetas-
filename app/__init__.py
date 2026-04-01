# archivo especial por eso los guines bajos
# especial para configurar flask, solo importar cosas para iniciar programa, define la carpeta como el cerebro del proyecto

from flask import Flask
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
CORS(app)

from app.routes import login
from app.routes import receta

@app.route('/')
def home():
    return render_template("index.html")