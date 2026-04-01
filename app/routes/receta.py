# Archivo para endpoints de Receta CRUD

from app import app
from flask import request, jsonify
import sqlite3
from app.auth import token_required
from app.utils import guardar_historial


# GET
@app.route('/receta', methods=['GET'])
@token_required
def get_items(user_id):
    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()

    nombre = request.args.get("nombre")
    ingredientes = request.args.get("ingredientes")
    categoria = request.args.get("categoria")

    if nombre:
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND nombre=?", (user_id, nombre))
    elif ingredientes: 
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND ingredientes LIKE ?", (user_id, f"%{ingredientes}%"))
    elif categoria:  
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND categoria LIKE ?", (user_id, f"%{categoria}%"))
    else:  
        cursor.execute("SELECT * FROM receta WHERE user_id=?", (user_id,))
    
    rows = cursor.fetchall()
    conn.close()

    receta = [{"id": r[0], "nombre": r[2]} for r in rows]

    return jsonify({"receta": receta}), 200


# POST
@app.route('/receta', methods=['POST'])
@token_required
def create_item(user_id):
    data = request.get_json()
    nombre = data.get("nombre")

    if not nombre:
        return jsonify({"message": "nombre obligatorio"}), 400

    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO receta (user_id, nombre) VALUES (?, ?)", (user_id, nombre))
    conn.commit()

    new_id = cursor.lastrowid

    guardar_historial("crear", {"id": new_id, "nombre": nombre})

    conn.close()

    return jsonify({"message": "creado"}), 201
