# Users API

API REST en Flask y SQLAlchemy con arquitectura `controller -> service -> repository -> database`.

## Ejecutar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Por defecto usa `sqlite:///users.db`. Define `DATABASE_URL` para cambiar la base de datos.

## Rutas

- `POST, GET /users`; `GET, PUT, DELETE /users/<user_id>`
- `PUT /users/<user_id>/profile`
- `POST, DELETE /users/<user_id>/skills/<skill_id>`
- `POST /users/<user_id>/posts`; `GET /posts`; `GET, PUT, DELETE /posts/<post_id>`
- `POST, GET /skills`; `GET /skills/<skill_id>`

## Verificación

```bash
pytest
newman run postman/UsersApi.postman_collection.json -e postman/Local.postman_environment.json
```
