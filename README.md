Recetify API Rest - Full Stack

API REST desarrollada con Flask que permite gestionar recetas mediante operaciones CRUD, con autenticación basada en JWT.

Incluye backend modularizado y futuro frontend en HTML, CSS y JavaScript.

CARACTERISTICAS

- CRUD completo de recetas
- Autenticación con JWT
- Base de datos SQLite
- Arquitectura modular (en progreso)
- Historial de cambios (en desarrollo)
- Integración futura con frontend

TECNOLOGIAS

- Python
- Flask
- SQLite
- JWT (JSON Web Tokens)
- HTML, CSS, JavaScript (en desarrollo)

ESTRUCTURA 

App/
  __init__.py
  routes/
    auth.py
    recetas.py
  auth.py
  models.py
data/
static/
templates/
tests/
requeriments.txt
run.py
.gitignore

AUTENTICACION



ENDPOINTS

AUTH
POST /register
POST /login

RECETAS
GET /receta
POST /receta
PUT /receta/<id>
DELETE /receta/<id>
