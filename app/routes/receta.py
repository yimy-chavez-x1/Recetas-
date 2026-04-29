# Archivo para endpoints de Receta CRUD

from app import app
from flask import request, jsonify
import sqlite3
from app.auth import token_required
from app.utils import guardar_historial
from app.models import get_db_connection


# GET
@app.route('/receta', methods=['GET'])
@token_required
def get_items(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    nombre = request.args.get("nombre")
    ingredientes = request.args.get("ingredientes")
    preparacion = request.args.get("preparacion")

    if nombre:
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND nombre=?", (user_id, nombre))
    elif ingredientes: 
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND ingredientes LIKE ?", (user_id, f"%{ingredientes}%"))
    elif preparacion:
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND preparacion LIKE ?", (user_id, f"%{preparacion}%"))
    else:
        cursor.execute("SELECT * FROM receta WHERE user_id=?", (user_id,))
    
    rows = cursor.fetchall()
    conn.close()

    receta = [
        {
        "id": r["id"],
        "nombre": r["nombre"],
        "ingredientes": r["ingredientes"],
        "preparacion": r["preparacion"]
        }     
        for r in rows
    ]

    return jsonify({"receta": receta}), 200


# POST
@app.route('/receta', methods=['POST'])
@token_required
def create_item(user_id):
    data = request.get_json()
    nombre = data.get("nombre")
    ingredientes = data.get("ingredientes")
    preparacion = data.get("preparacion")

    if not nombre:
        return jsonify({"message": "nombre obligatorio"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO receta (user_id, nombre, ingredientes, preparacion) VALUES (?, ?, ?, ?)", (user_id, nombre, ingredientes, preparacion))
    conn.commit()

    conn.close()

    return jsonify({"message": "creado"}), 201

# PUT /receta/<id>
@app.route('/receta/<int:receta_id>', methods=['PUT'])
@token_required
def update_item(receta_id, user_id):
    '''
    Actualizar una receta por ID
    ---
    tags:
      - Items
    security:
      - Bearer: []
    parameters:
      - in: path
        name: receta_id
        required: true
        type: integer
      - in: body
        name: item
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
            ingredientes:
              type: string
            duracion:
              type: string
            preparacion:
              type: string
    responses:
      200:
        description: Receta actualizada
      404:
        description: Receta no encontrada
    '''
    data = request.get_json()
    nombre = data.get("nombre")
    ingredientes = data.get("ingredientes")
    preparacion = data.get("preparacion")


    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM receta WHERE id = ? AND user_id = ?", (receta_id,user_id))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"message": "Receta no encontrada"}), 404

    cursor.execute("UPDATE receta SET nombre = ?, ingredientes = ?, preparacion = ? WHERE id = ? AND user_id = ?", (nombre, ingredientes, preparacion, receta_id, user_id))
    conn.commit()
    guardar_historial("actualizar", {
    "id": receta_id,
    "user_id": user_id,
    "nombre": nombre,
    "ingredientes": ingredientes,
    "preparacion": preparacion,
    })

    conn.close()

    return jsonify({"message": "Receta actualizada", "receta": {"id": receta_id, "user_id": user_id, "nombre": nombre, "ingredientes": ingredientes, "preparacion": preparacion}}), 200


# DELETE /receta/<id>
@app.route('/receta/<int:receta_id>', methods=['DELETE'])
@token_required
def delete_item(receta_id, user_id):
    '''
    Eliminar una receta por ID
    ---
    tags:
      - Items
    security:
      - Bearer: []
    parameters:
      - in: path
        name: receta_id
        required: true
        type: integer
    responses:
      200:
        description: Receta eliminada
      404:
        description: Receta no encontrada
    '''
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM receta WHERE id = ? AND user_id = ?", (receta_id, user_id))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"message": "Receta no encontrada"}), 404

    cursor.execute("DELETE FROM receta WHERE id = ? AND user_id = ?", (receta_id, user_id))
    conn.commit()
  
    conn.close()

    return jsonify({
        "message": "Receta eliminada",
          "receta": {
        "id": row["id"],
        "user_id": row["user_id"],
        "nombre": row["nombre"],
        "ingredientes": row["ingredientes"],
        "preparacion": row["preparacion"],
        "favorito": row["favorito"]
    }}), 200
    