---
name: rest-api
description: REST API design guidance. Use when creating or changing HTTP endpoints, resources, status codes, validation, or API contracts.
---

# REST API

Utilizar apropiadamente los métodos:

GET
POST
PUT
PATCH
DELETE

## Status codes

200 OK
Operación exitosa.

201 Created
Recurso creado.

204 No Content
Eliminación exitosa sin cuerpo.

400 Bad Request
Datos inválidos.

404 Not Found
Recurso inexistente.

409 Conflict
Conflicto con el estado actual del sistema.

500 Internal Server Error
Error inesperado.

No retornar 200 para todas las situaciones.

No retornar directamente entidades SQLAlchemy.

Utilizar DTOs para entrada y salida.
