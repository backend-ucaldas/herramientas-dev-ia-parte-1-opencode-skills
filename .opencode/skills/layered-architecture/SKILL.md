---
name: layered-architecture
description: Layered architecture guidance. Use when designing or changing controllers, services, repositories, models, DTOs, mappers, or persistence boundaries.
---

# Layered Architecture

Flujo principal del backend:

Controller
↓
Service
↓
Repository
↓
Database

El mapper es un componente de apoyo utilizado por el service para transformar datos entre DTOs y modelos. No reemplaza ninguna de las capas anteriores ni accede a la base de datos.

## Controller

Responsabilidades:

- recibir solicitudes HTTP;
- leer parámetros;
- llamar al service;
- construir respuestas HTTP.

No debe:

- acceder directamente a la base de datos;
- realizar consultas a la base de datos;
- contener reglas de negocio.

## Service

Responsabilidades:

- implementar reglas de negocio;
- coordinar operaciones;
- utilizar repositories.

No debe depender de conceptos HTTP.

## Repository

Responsabilidades:

- consultar;
- guardar;
- actualizar;
- eliminar información.

El acceso a persistencia debe estar encapsulado aquí.

## Models

Representan entidades persistentes.

## DTO

Representan información de entrada y salida.

## Mappers

Se encargan de transformar objetos entre las capas de la aplicación, principalmente:

- convertir modelos persistentes en DTOs de salida;
- convertir DTOs de entrada en modelos o datos para el repository;
- centralizar la correspondencia entre nombres, formatos y estructuras de datos.

No deben:

- contener reglas de negocio;
- acceder a la base de datos;
- depender de conceptos HTTP;
- ejecutar consultas ni modificar información persistente.

Los mappers deben ser simples, predecibles y fáciles de probar. Cuando una transformación requiera una decisión de negocio, esta debe permanecer en el service.

## Ejemplo de mapper

Crear, por ejemplo:

```text
app/mappers/user_mapper.py
```

El mapper transforma los datos, pero no guarda ni consulta información:

```python
def user_to_response_dto(user):
    return UserResponseDTO(
        id=user.id,
        name=user.name,
        email=user.email,
    )


def user_create_dto_to_model(data):
    return User(
        name=data.name,
        email=data.email,
    )
```

El service coordina el flujo y utiliza el mapper; el repository sigue siendo responsable de persistir:

```text
Controller recibe JSON
        ↓
DTO de entrada → Mapper → Modelo
                         ↓
                    Repository → Database
                         ↓
DTO de salida ← Mapper ← Modelo
        ↓
Controller construye la respuesta HTTP
```

Los nombres de DTO y campos del ejemplo deben ajustarse a las clases reales del proyecto. El mapper no debe decidir reglas como si un correo ya está registrado; esa validación corresponde al service.

## SOLID

Aplicar especialmente:

S — Single Responsibility Principle.

Cada clase debe tener una responsabilidad principal.

D — Dependency Inversion Principle.

Las capas superiores no deben depender directamente
de detalles de infraestructura.