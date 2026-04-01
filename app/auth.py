#archivo solo para login y seguridad

from flask import request, jsonify
import jwt, os, datetime
from functools import wraps
from app import app

CLAVE = os.getenv("SECRET_KEY", "dev_key")

def generar_token(user_id):
    return jwt.encode({
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, CLAVE, algorithm="HS256")


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

    return decorator