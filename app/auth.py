#archivo solo para login y seguridad

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt