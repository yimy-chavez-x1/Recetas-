from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3, json, os, jwt, datetime


app = Flask(__name__)
DATABASE = 'recetas.db'
CLAVE='secreto'
CORS(app)


# Directorio para almacenar historiales en JSON
HISTORIAL_DIR = "data"
os.makedirs(HISTORIAL_DIR, exist_ok=True)


# Crear la base de datos 
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS receta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            ingredientes TEXT,
            duracion TEXT,
            preparacion TEXT,
            anotacion TEXT,
            categoria TEXT,
            favorito TEXT DEFAULT 'no' CHECK(favorito IN ('si','no')),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
        conn.commit()
init_db()


def crear_usuario(username,email,password):
    conn = get_db_connection()
    hash_pw = generate_password_hash(password)
    conn.execute('INSERT INTO users (username,email ,password) VALUES (?, ?, ?)', (username,email, hash_pw))
    conn.commit()

    conn.close()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"mensaje": "Falta token"}), 401
        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]
            payload = jwt.decode(token, CLAVE, algorithms=["HS256"])
            user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"mensaje": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"mensaje": "Token inválido"}), 401
        return f(user_id=user_id, *args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

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
    '''
    Iniciar sesión y obtener token JWT
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: credenciales
        required: true
        schema:
          type: object
          properties:
            usuario:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Token JWT generado exitosamente
      401:
        description: Credenciales inválidas
    '''


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
        }, CLAVE, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"mensaje": "Credenciales inválidas"}), 401
# Esto ya esta agregado en auth.py 


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row 
    return conn


@app.route('/receta', methods=['GET'])
@token_required
def get_items(user_id):
    '''
    Obtener todas las recetas
    ---
    tags:
      - Items
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de todas las recetas
    '''
    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()

    nombre = request.args.get("nombre")
    ingredientes = request.args.get("ingredientes")
    categoria = request.args.get("categoria")

    if nombre:
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND nombre=? ORDER BY favorito DESC", (user_id, nombre))
    elif ingredientes: 
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND ingredientes LIKE ? ORDER BY favorito DESC", (user_id, f"%{ingredientes}%"))
    elif categoria:  
        cursor.execute("SELECT * FROM receta WHERE user_id=? AND categoria LIKE ? ORDER BY favorito DESC", (user_id, f"%{categoria}%"))
    else:  
        cursor.execute("SELECT * FROM receta WHERE user_id=? ORDER BY favorito DESC", (user_id,))
    
    rows = cursor.fetchall()
    conn.close()

    receta = [{"id": row[0], "user_id": row[1], "nombre": row[2], "ingredientes": row[3], "duracion":row[4], "preparacion":row[5], "anotacion":row[6],"categoria":row[7],"favorito":row[8]} for row in rows]
    return jsonify({"receta": receta}), 200


# POST /receta
@app.route('/receta', methods=['POST'])
@token_required
def create_item(user_id):
    '''
    Crear una nueva receta
    ---
    tags:
      - Items
    security:
      - Bearer: []
    parameters:
      - in: body
        name: item
        required: true
        schema:
          type: object
          required:
            - nombre
          
          properties:
            nombre:
              type: string
            ingredientes:
              type: string
            duracion:
              type: string
            preparacion:
              type: string
            anotacion:
              type: string
            categoria:
              type: string
            favorito:
              type: string
    responses:
      201:
        description: Receta creada exitosamente
      400:
        description: Los campos son obligatorios
    '''
    data = request.get_json()
    nombre = data.get("nombre")
    ingredientes = data.get("ingredientes")
    duracion = data.get("duracion")
    preparacion = data.get("preparacion")
    anotacion = data.get("anotacion")
    categoria = data.get("categoria")
    favorito = data.get("favorito")


    if not nombre:
        return jsonify({"message": "El campo 'nombre' es obligatorio"}), 400

    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO receta (user_id, nombre, ingredientes,duracion,preparacion,anotacion,categoria,favorito) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_id, nombre, ingredientes, duracion, preparacion, anotacion, categoria, favorito))
    conn.commit()
    new_id = cursor.lastrowid

    guardar_historial("crear", {
    "id": new_id,
    "user_id": user_id,
    "nombre": nombre,
    "ingredientes": ingredientes,
    "duracion": duracion,
    "preparacion": preparacion,
    "anotacion":anotacion,
    "categoria":categoria,
    "favorito":favorito
    })

    conn.close()

    return jsonify({"message": "Receta creada", "receta": {"id": new_id,"user_id":user_id, "nombre": nombre, "ingredientes": ingredientes, "duracion":duracion, "preparacion": preparacion, "anotacion": anotacion,"categoria": categoria, "favorito":favorito}}), 201
  
  

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
            anotacion:
              type: string
            categoria:
              type: string
            favorito:
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
    duracion = data.get("duracion")
    preparacion = data.get("preparacion")
    anotacion = data.get("anotacion")
    categoria = data.get("categoria")
    favorito = data.get("favorito")

    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM receta WHERE id = ? AND user_id = ?", (receta_id,user_id))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"message": "Receta no encontrada"}), 404

    cursor.execute("UPDATE receta SET nombre = ?, ingredientes = ?, duracion = ?, preparacion = ?,anotacion = ?, categoria = ?, favorito = ? WHERE id = ? AND user_id = ?", (nombre, ingredientes, duracion, preparacion,anotacion,categoria,favorito, receta_id, user_id))
    conn.commit()
    guardar_historial("actualizar", {
    "id": receta_id,
    "user_id": user_id,
    "nombre": nombre,
    "ingredientes": ingredientes,
    "duracion": duracion,
    "preparacion": preparacion,
    "anotacion":anotacion,
    "categoria":categoria,
    "favorito":favorito
    })

    conn.close()

    return jsonify({"message": "Receta actualizada", "receta": {"id": receta_id, "user_id": user_id, "nombre": nombre, "ingredientes": ingredientes, "duracion":duracion,"preparacion": preparacion,"anotacion":anotacion, "categoria":categoria, "favorito":favorito}}), 200


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
    conn = sqlite3.connect("recetas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM receta WHERE id = ? AND user_id = ?", (receta_id, user_id))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({"message": "Receta no encontrada"}), 404

    cursor.execute("DELETE FROM receta WHERE id = ? AND user_id = ?", (receta_id, user_id))
    conn.commit()

    guardar_historial("eliminar", {
    "id": row[0],
    "user_id": row[1],
    "nombre": row[2],
    "ingredientes": row[3],
    "duracion": row[4],
    "preparacion": row[5],
    "anotacion":row[6],
    "categoria":row[7],
    "favorito":row[8]
    })

    conn.close()

    return jsonify({"message": "Receta eliminada", "receta": {"id": row[0],"user_id":row[1], "nombre": row[2], "ingredientes": row[3], "duracion":row[4], "preparacion":row[5], "anotacion":row[6],"categoria":row[7],"favorito":row[8]}}), 200
    

def ruta_historial():
    return os.path.join(HISTORIAL_DIR, "apiREST(Recetify).json")

def cargar_historial():
  ruta = ruta_historial()
  if os.path.exists(ruta):
    try:
      with open(ruta, "r", encoding="utf-8") as f:             
        return json.load(f)
    except Exception:
      return []
  return []
  
def guardar_historial(accion, receta):
  historial = cargar_historial()
  entrada = {
        "accion": accion,
        "receta": receta,
        "timestamp": datetime.datetime.now().isoformat()
    }
  historial.append(entrada)
  try:
      with open(ruta_historial(), "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
  except Exception as e:
        print(f"Error al guardar historial: {e}")



# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
