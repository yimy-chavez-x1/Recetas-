#archivo para datos y database
import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'recetas.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

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

    conn.commit()
    conn.close()

def crear_usuario(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hash_pw = generate_password_hash(password)

    cursor.execute(
        'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
        (username, email, hash_pw)
    )

    conn.commit()
    conn.close()

