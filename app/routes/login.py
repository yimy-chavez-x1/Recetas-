# Archivo para endpoints de autentificación

from app import app  # conecta con el  __init__
from flask import request, jsonify
import sqlite3

from werkzeug.security import check_password_hash
from app.models import crear_usuario, get_db_connection
from app.auth import generar_token

# Registro
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


# Inicio de Sesion
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    correo = data.get('email')
    password = data.get('password')

    if not correo or not password:
        return jsonify({"mensaje": "Email y password son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password FROM users WHERE email = ?",
        (correo,)
    )
    row = cursor.fetchone()

    conn.close()

    if row and check_password_hash(row["password"], password):
        token = generar_token(row["id"])
        return jsonify({"token": token})

    return jsonify({"mensaje": "Credenciales inválidas"}), 401