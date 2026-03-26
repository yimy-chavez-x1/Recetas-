#archivo para endpoints

from flask import request, jsonify
import sqlite3, jwt, datetime
from werkzeug.security import check_password_hash
from app import app  # conecta con el  __init__
from app.models import crear_usuario

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    usuario = data.get("username")
    correo = data.get("email")
    password = data.get("password")

    if not usuario or not correo or not password:
        return jsonify({"mensaje": "Faltan campos"}), 400

    try:
        crear_usuario(usuario, correo, password)
        return jsonify({"mensaje": "Usuario creado"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"mensaje": "El email ya está registrado"}), 400
    except Exception:
        return jsonify({"mensaje": "Error"}), 500


@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json()
    correo = datos.get('email')
    password = datos.get('password')

    if not correo or not password:
        return jsonify({"mensaje": "Email y password son obligatorios"}), 400

    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE email = ?", (correo,))
    row = cursor.fetchone()
    conn.close()

    if row and check_password_hash(row[1], password):
        token = jwt.encode({
            "user_id": row[0],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, "secreto", algorithm="HS256")  # por ahora dejamos esto así

        return jsonify({"token": token})

    return jsonify({"mensaje": "Credenciales inválidas"}), 401

