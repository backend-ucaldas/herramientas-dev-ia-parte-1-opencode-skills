# Guía práctica: OpenCode + Skills + Agentes

## Objetivo

Construir una API REST utilizando OpenCode y aplicar conceptos vistos previamente en clase:

* arquitectura por capas;
* códigos de estado HTTP;
* principios SOLID S y D;
* relaciones 1:1, 1:N y N:N;
* mappers para separar los DTOs de los modelos persistentes;
* Skills;
* agentes especializados;
* validación de arquitectura;
* pruebas básicas y casos límite.

La práctica busca que el estudiante utilice la IA como herramienta de desarrollo, pero manteniendo el control sobre las decisiones de ingeniería.

---

# 1. Caso de estudio

Se desarrollará una API con las siguientes entidades:

```text
User
- id
- name
- email

Profile
- id
- bio
- phone

Post
- id
- title
- content

Skill
- id
- name
```

Relaciones:

```text
User 1 ───── 1 Profile

User 1 ───── N Post

User N ───── N Skill
```

Interpretación:

```text
Un usuario tiene un perfil.

Un usuario puede tener muchas publicaciones.

Una publicación pertenece a un usuario.

Un usuario puede tener muchas habilidades.

Una habilidad puede pertenecer a muchos usuarios.
```

---

# 2. Crear e iniciar el proyecto en OpenCode

Crear la carpeta del proyecto y ubicarse en ella. OpenCode debe iniciarse desde la raíz del proyecto para trabajar sobre esa carpeta:

```bash
mkdir users-api
cd users-api
```

Ahora, desde la misma raíz (`users-api`), iniciar OpenCode:

```bash
opencode
```

Dentro de OpenCode, ejecutar:

```text
/init
```

Este comando ayuda a crear o actualizar `AGENTS.md` con instrucciones sobre el proyecto. Revise lo que generó y compleméntelo con las reglas de trabajo de esta guía. `AGENTS.md` contiene instrucciones generales del proyecto; no reemplaza las Skills ni las definiciones de los agentes.

Agregar en `AGENTS.md`, por ejemplo:

```markdown
# Instrucciones del proyecto

- Antes de diseñar o modificar la arquitectura, consulta
  `.opencode/skills/layered-architecture/SKILL.md`.
- Para cambios en endpoints, contratos HTTP o códigos de estado,
  consulta `.opencode/skills/rest-api/SKILL.md`.
- Para cambios en entidades o relaciones, consulta
  `.opencode/skills/relational-modeling/SKILL.md`.
- Para definir o ejecutar pruebas de integración de la API, consulta
  `.opencode/skills/testing/SKILL.md` y utiliza la colección Postman del proyecto.
- Cuando se solicite una revisión de arquitectura, usa el agente `@architect`.
- Cuando se solicite diseñar, generar o ejecutar pruebas de API, usa el agente
  `@tester`.
- No asumas que una revisión o ejecución ya se realizó: informa qué agente,
  colección y comandos utilizaste, y reporta los resultados observados.
```

Las Skills contienen conocimiento especializado y los agentes tienen responsabilidades concretas. OpenCode puede descubrirlos en `.opencode/skills/` y `.opencode/agents/`; las instrucciones anteriores indican cuándo consultarlos o invocarlos en el flujo de trabajo.

Si `/init` todavía no ha creado esas carpetas, créelas manualmente. En las siguientes secciones se agregarán los archivos de agentes y Skills:

```text
users-api/
├── .opencode/
│   ├── agents/
│   └── skills/
└── AGENTS.md        # creado o actualizado al ejecutar /init
```

Más adelante, al construir la API, se espera una estructura similar a esta:

```text
users-api/
│
├── .opencode/
│   ├── agents/
│   └── skills/
│
├── app/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── dtos/
│   ├── mappers/
│   └── config/
│
├── tests/            # pruebas unitarias opcionales, por ejemplo para mappers
├── postman/
│   ├── UsersApi.postman_collection.json
│   └── Local.postman_environment.json
├── requirements.txt
└── app.py
```

---

# 3. Reflexionemos antes: desarrollar sin Skills

Si se solicita inicialmente:

```text
Crea una API REST con Flask para gestionar usuarios,
perfiles, publicaciones y habilidades.

Relaciones:

User 1-1 Profile
User 1-N Post
User N-N Skill

Usa SQLAlchemy.
```

Una vez generado el código, analizarlo.

Responder:

```text
¿Existe realmente una arquitectura por capas?

¿El controller contiene lógica de negocio?

¿El controller accede directamente a SQLAlchemy?

¿Existe una capa repository?

¿Se utilizan mappers para convertir entre DTOs y modelos?

¿Las relaciones están correctamente implementadas?

¿Se utilizan correctamente los códigos HTTP?

¿Las clases tienen responsabilidades claras?
```

Objetivo:

```text
PROMPT
  ↓
 IA
  ↓
CÓDIGO FUNCIONAL

pero

CÓDIGO FUNCIONAL ≠ BUENA ARQUITECTURA
```

---

# 4. Crear las Skills

Crear la siguiente estructura:

```text
.opencode/
├── agents/
│   ├── architect.md
│   └── tester.md
│
└── skills/
    ├── layered-architecture/
    │   └── SKILL.md
    │
    ├── rest-api/
    │   └── SKILL.md
    │
    ├── relational-modeling/
    │   └── SKILL.md
    │
    └── testing/
        └── SKILL.md
```

Una Skill representa conocimiento reutilizable.

```text
SKILL
=
reglas que la IA debe conocer
```

---

# 5. Skill: arquitectura por capas

Crear:

```text
.opencode/skills/layered-architecture/SKILL.md
```

Contenido:

````markdown
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

````

---

# 6. Skill: REST

Crear:

```text
.opencode/skills/rest-api/SKILL.md
```

Contenido:

```markdown
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

```

---

# 7. Skill: modelado relacional

Crear:

```text
.opencode/skills/relational-modeling/SKILL.md
```

Contenido:

```markdown
---
name: relational-modeling
description: Relational data modeling guidance. Use when designing database tables, keys, relationships, constraints, indexes, or migrations.
---

# Relational Modeling

Implementar las relaciones utilizando bases de datos relacionales.

## One-to-One

User 1-1 Profile

Profile debe tener:

user_id

como foreign key y UNIQUE.

## One-to-Many

User 1-N Post

Post debe contener:

user_id

como foreign key.

## Many-to-Many

User N-N Skill

Crear una tabla intermedia:

user_skills

con:

user_id
skill_id
```


---

# 8. Skill: pruebas

Crear:

```text
.opencode/skills/testing/SKILL.md
```

Contenido:

````markdown
---
name: testing
description: Postman API integration testing guidance. Use when designing, generating, reviewing, or executing Postman collections to validate REST endpoints.
---

# Postman Integration Testing

El enfoque principal para validar la API son pruebas de integración HTTP
ejecutadas con Postman. Las pruebas deben enviar solicitudes reales a la
aplicación en ejecución y comprobar el comportamiento observable de los
endpoints.

## Artefactos requeridos

Generar y mantener dentro del proyecto:

- `postman/UsersApi.postman_collection.json`: colección importable en Postman.
- `postman/Local.postman_environment.json`: environment local con la URL base
  de la API y variables necesarias para compartir IDs entre solicitudes.

La colección debe ser JSON válido con formato compatible con Postman
Collection v2.1. No incluir secretos ni depender de valores locales fijos.
Usar variables como `{{baseUrl}}`, `{{userId}}`, `{{postId}}` y `{{skillId}}`.

## Cobertura por endpoint

Para cada endpoint, incluir los casos aplicables:

1. Happy path.
2. Entrada inválida o campos requeridos ausentes.
3. Recurso inexistente (404).
4. Conflicto, por ejemplo un email duplicado (409).
5. Relaciones y casos límite relevantes.

Cada solicitud debe incluir scripts de Postman (`pm.test`) que validen al
menos el código HTTP y, cuando aplique, el cuerpo, los encabezados y los datos
devueltos. Organizar las solicitudes con nombres claros y agruparlas por
recurso o flujo.

## Datos y orden de ejecución

- Definir el método, URL, headers y body de cada solicitud.
- Utilizar variables de colección/environment para la URL y los IDs.
- Guardar IDs de recursos creados desde los scripts de respuesta con
  `pm.environment.set(...)` o `pm.collectionVariables.set(...)`.
- Ordenar las solicitudes para crear primero los recursos que otras pruebas
  necesitan.
- Mantener las pruebas repetibles: indicar los datos requeridos y evitar
  depender de ejecuciones previas. Limpiar o usar datos únicos cuando sea
  necesario.
- No crear endpoints especiales solo para pruebas; probar los endpoints
  funcionales de la API.

## Ejecutar y reportar

Ejecutar la colección con el Collection Runner de Postman usando el environment
local. También se puede usar Newman desde la terminal:

```bash
newman run postman/UsersApi.postman_collection.json \
  -e postman/Local.postman_environment.json
```

Informar cuántas pruebas pasaron y fallaron. Para cada fallo, reportar la
solicitud, la aserción fallida, el resultado esperado y el resultado recibido.
No cambiar código productivo para ocultar una prueba fallida.

## Alcance de las pruebas unitarias

Postman valida la integración observable de la API; no comprueba directamente
funciones internas como los mappers. Si se requiere validar conversiones de
mappers, conservar pruebas unitarias separadas con pytest en `tests/`.


---

Ejemplo mínimo de una colección Postman v2.1. El agente Tester debe generar
una colección completa, con requests para los endpoints y escenarios de la
matriz; este ejemplo solo muestra el formato JSON y una aserción:

```json
{
  "info": {
    "name": "Users API - ejemplo",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Listar usuarios",
      "request": {
        "method": "GET",
        "header": [],
        "url": "{{baseUrl}}/users"
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "type": "text/javascript",
            "exec": [
              "pm.test('Responde HTTP 200', function () {",
              "    pm.response.to.have.status(200);",
              "});"
            ]
          }
        }
      ]
    }
  ]
}
```

La variable `baseUrl` se define en el environment local, por ejemplo como
`http://127.0.0.1:5000`. Ajustar la ruta y el status esperado al contrato real
de la API.
````
---

# 9. Planificación de la aplicación utilizando Skills

## Construir plan 

Solicitar en open code con la consola de tipo "Plan" en primer lugar, con el fin que la IA pregunte detalles que aún no han quedado claros:

```text
Construye una API REST en Flask para gestionar:

User
Profile
Post
Skill

Usa SQLAlchemy.

Aplica las skills disponibles de:

- layered-architecture
- relational-modeling
- rest-api
- testing

Relaciones:

User 1-1 Profile
User 1-N Post
User N-N Skill

Implementa CRUD para User y Post.

Implementa además:

- asignar Profile a User;
- asignar Skill a User;
- eliminar Skill de User.

```

## Verificar plan

Luego del plan se deben de responder las dudas que tiene la IA antes de continuar con la implementación de código

# 10. Solicitar implementación al builder

Luego de tener claro lo que la IA entendió según el plan, pasamos a modo builder y se inicia la codificación. Solicitar que implemente lo aprobado en el plan y verificar que todo esté en orden

---

# 11. Endpoints esperados

## User

```http
POST   /users
GET    /users
GET    /users/{id}
PUT    /users/{id}
DELETE /users/{id}
```

## Profile

```http
POST /users/{id}/profile
GET  /users/{id}/profile
```

## Post

```http
POST   /users/{id}/posts
GET    /users/{id}/posts
GET    /posts/{id}
PUT    /posts/{id}
DELETE /posts/{id}
```

## Skill

```http
POST /skills
GET  /skills
```

Asignar:

```http
POST /users/{user_id}/skills/{skill_id}
```

Eliminar relación:

```http
DELETE /users/{user_id}/skills/{skill_id}
```

---

# 12. Incorporar el agente Architect

Hasta este punto las Skills contienen las reglas.

Ahora se crea un agente cuya responsabilidad sea utilizarlas para revisar la arquitectura.

```text
SKILL
=
qué reglas conozco

AGENT
=
qué responsabilidad tengo
```

Crear:

```text
.opencode/agents/architect.md
```

Contenido:

```markdown
---
description: Diseña la arquitectura de aplicaciones y evalúa las ventajas y desventajas de las decisiones técnicas.
mode: subagent
permission:
  edit: deny
  bash: deny
---

# Agente arquitecto

## Rol

Eres un arquitecto de software.

Tu responsabilidad es validar la arquitectura del proyecto existente.

No implementes funcionalidades salvo que se solicite explícitamente.

Utiliza las skills disponibles relacionadas con:

- arquitectura por capas;
- modelado relacional;
- REST cuando afecte a la arquitectura.

## Validación

### Arquitectura por capas

Flujo esperado de dependencias:

Controlador → Servicio → Repositorio → Base de datos

El servicio puede utilizar un mapper para convertir entre DTOs y modelos antes o después de llamar al repositorio. El mapper no es una capa de persistencia.

Verifica que los controladores no accedan directamente a SQLAlchemy.

Verifica que los controladores no implementen reglas de negocio.

Verifica que los servicios coordinen la lógica de negocio.

Verifica que los repositorios encapsulen la persistencia.

Verifica que los mappers transformen DTOs y modelos sin contener reglas de negocio, manejo de HTTP ni operaciones de persistencia.

Verifica que los servicios utilicen mappers cuando los datos se conviertan entre DTOs y modelos, y que la lógica de mapeo no se duplique en controladores o repositorios.

### SOLID S: principio de responsabilidad única

Verifica que las clases tengan una única responsabilidad claramente definida.

Detecta clases que combinen:

- manejo de HTTP;
- lógica de negocio;
- persistencia.

### SOLID D: principio de inversión de dependencias

Verifica que los componentes de alto nivel no estén fuertemente acoplados a los detalles de persistencia.

### Modelo relacional

Verifica las claves foráneas, las restricciones de unicidad y las tablas de asociación.

## Salida

Devuelve un informe que contenga:

1. Decisiones arquitectónicas correctas.
2. Incumplimientos de la arquitectura.
3. Incumplimientos de los principios SOLID.
4. Problemas de modelado relacional.
5. Uso de mappers y problemas de mapeo.
6. Correcciones recomendadas.

No modifiques el código automáticamente.
```

---

# 13. Ejecutar el Architect

Solicitar:

```text
Usa el agente @architect para revisar
la arquitectura actual del proyecto.

No modifiques código.

Indica:

- errores de arquitectura;
- uso incorrecto o ausencia de mappers para convertir DTOs y modelos;
- violaciones de SOLID S;
- violaciones de SOLID D;
- problemas en las relaciones;
- cambios recomendados.
```

El estudiante debe analizar el reporte.

Ejemplo de error:

```python
class UserController:

    def get_users(self):
        return User.query.all()
```

Problema:

```text
Controller
   ↓
Database
```

Esperado:

```text
Controller
   ↓
Service
   ↓
Repository
   ↓
Database
```

El flujo también debe utilizar un mapper cuando se convierten datos entre DTOs y modelos; esta transformación no debe quedar duplicada en el controller ni en el repository.

---

# 14. Corregir la arquitectura

Después de revisar el informe:

```text
Corrige únicamente los problemas identificados
por el agente architect.

Mantén las funcionalidades actuales.
```

Después volver a ejecutar el agente:

```text
Revisa nuevamente la arquitectura
y determina si los problemas fueron corregidos.
```

Esto introduce un ciclo:

```text
IMPLEMENTAR
    ↓
REVISAR
    ↓
CORREGIR
    ↓
VOLVER A REVISAR
```

---

# 15. Incorporar el agente Tester

Ahora crear un segundo agente.

Crear:

```text
.opencode/agents/tester.md
```

Contenido:

````markdown
---
description: Revisa y valida el comportamiento de la aplicación mediante pruebas específicas.
mode: subagent
---

# Agente de pruebas

## Rol

Eres un profesional de pruebas de software responsable de validar la API REST.

Utiliza las skills disponibles relacionadas con REST y pruebas de software.

Tu responsabilidad principal es diseñar, generar y ejecutar pruebas de integración de la API REST en Postman.

## Para cada endpoint, identifica

1. El comportamiento esperado, el método HTTP y la URL.
2. El caso exitoso, las entradas inválidas, los recursos no encontrados, los conflictos y los casos límite relevantes.
3. El código de estado esperado, el cuerpo de la respuesta, los encabezados y los efectos observables.
4. La preparación necesaria y el orden de las solicitudes para los recursos dependientes.

Genera los siguientes archivos importables en Postman:

- `postman/UsersApi.postman_collection.json` utilizando el formato Postman Collection v2.1.
- `postman/Local.postman_environment.json` con `baseUrl` y las variables necesarias.

Cada solicitud debe incluir scripts de prueba de Postman que utilicen `pm.test` para comprobar el código de estado y los datos relevantes de la respuesta.

Utiliza variables como `{{baseUrl}}` y guarda los identificadores generados en el entorno para utilizarlos en solicitudes posteriores.

No agregues endpoints exclusivos para pruebas; utiliza los endpoints de la API definidos por el proyecto.

Las pruebas de conversión de los mappers son pruebas unitarias, no pruebas de integración en Postman. Mantenlas separadas en pytest únicamente cuando el proyecto requiera cobertura unitaria.

## Categorías de pruebas

### Caso exitoso

Ejemplo:

POST /users

Datos de entrada:

```json
{
  "name": "Ana",
  "email": "ana@email.com"
}
```

Resultado esperado:

201 Created — Recurso creado.

### Entrada inválida

Prueba los siguientes casos:

- Nombre ausente.
- Correo electrónico ausente.
- Nombre vacío.
- Correo electrónico con formato inválido.

Resultado esperado:

400 Bad Request — Solicitud incorrecta.

### Recurso no encontrado

Ejemplo:

GET /users/999999

Resultado esperado:

404 Not Found — Recurso no encontrado.

### Conflicto

Crea dos usuarios con el mismo correo electrónico.

Resultado esperado:

409 Conflict — Conflicto.

### Relaciones

Verifica las siguientes relaciones:

#### Usuario 1-1 Perfil

Un usuario no puede tener dos perfiles.

#### Usuario 1-N Publicación

Un usuario puede tener varias publicaciones.

Cada publicación debe pertenecer al usuario correcto.

#### Usuario N-N Habilidad

Un usuario puede tener varias habilidades.

Una habilidad puede pertenecer a varios usuarios.

Verifica que no existan relaciones duplicadas entre un usuario y una habilidad.

### Comprobaciones en Postman

Para una solicitud exitosa `POST /users`, la colección debe comprobar el código de estado de creación y guardar el identificador devuelto para solicitudes posteriores.

Por ejemplo, agrega un script posterior a la respuesta en la sección `Post-response` similar al siguiente:

```javascript
pm.test("Crea un usuario", function () {
    pm.response.to.have.status(201);
});

const usuario = pm.response.json();

pm.test("La respuesta incluye el identificador del usuario", function () {
    pm.expect(usuario).to.have.property("id");
});

pm.environment.set("userId", usuario.id);
```
````

---

# 15. Pedir al Tester que diseñe las pruebas

Primero no generar código.

Solicitar:

```text
Usa el agente @tester.

Analiza los endpoints existentes.

No escribas todavía las pruebas.

Construye una matriz de casos de prueba
indicando:

- endpoint;
- escenario;
- entrada;
- resultado esperado;
- código HTTP esperado;
- aserciones de Postman;
- datos requeridos y variables que deben guardarse para el siguiente request.

Después de aprobar la matriz, genera la colección importable
`postman/UsersApi.postman_collection.json` (Postman Collection v2.1) y el
environment `postman/Local.postman_environment.json`. No modifiques código
productivo para agregar endpoints especiales de prueba.
```

Ejemplo:

| Endpoint       | Caso           | Resultado    | HTTP |
| -------------- | -------------- | ------------ | ---: |
| POST /users    | usuario válido | crea usuario |  201 |
| POST /users    | email vacío    | rechaza      |  400 |
| POST /users    | email repetido | conflicto    |  409 |
| GET /users/999 | no existe      | error        |  404 |

---

# 16. Identificar casos límite

El Tester debe definir también casos menos evidentes.

Ejemplos:

### User

```text
Nombre vacío.

Nombre solamente con espacios.

Email duplicado.

Email con formato inválido.

ID negativo.

ID inexistente.
```

### Profile

```text
Crear un segundo Profile
para un User que ya tiene uno.
```

Esperado:

```text
409 Conflict
```

### Post

```text
Crear Post para User inexistente.

Título vacío.

Contenido vacío.

Consultar Post inexistente.
```

### Skill

```text
Asignar Skill inexistente.

Asignar Skill a User inexistente.

Asignar dos veces la misma Skill al mismo User.

Eliminar una Skill que el usuario no posee.
```

---

# 17. Generar la colección de Postman

Después de revisar la matriz:

```text
Usa el agente @tester para generar los artefactos Postman
a partir de la matriz aprobada:

- `postman/UsersApi.postman_collection.json`
- `postman/Local.postman_environment.json`

La colección debe ser JSON válido e importable en Postman
(Collection v2.1). Incluye los requests de ensayo para los endpoints
existentes y scripts `pm.test` para validar status y respuestas.
Usa `{{baseUrl}}` y variables para compartir IDs entre requests.

No modifiques el código productivo ni crees endpoints solo para pruebas.
Si también se requieren pruebas unitarias de mappers, mantenlas separadas
en `tests/` con pytest.
```

---

# 18. Ejecutar la colección y validar resultados

1. Iniciar la API local.
2. Importar en Postman la colección y el environment generados.
3. Seleccionar el environment `Local` y comprobar que `baseUrl` apunta
   a la instancia local.
4. Ejecutar la colección con **Collection Runner** y revisar el resultado
   de cada request y de cada aserción.

Opcionalmente, ejecutar desde la terminal con Newman:

```bash
newman run postman/UsersApi.postman_collection.json `
  -e postman/Local.postman_environment.json
```

En PowerShell, el acento grave (`) permite continuar el comando en la
siguiente línea; también se puede escribir todo en una sola línea.

Clasificar los resultados:

```text
PASS
El endpoint respondió y las aserciones de Postman se cumplieron.

FAIL
Existe una diferencia entre
comportamiento esperado
e implementación.
```

Registrar el resumen del runner (requests ejecutados, pruebas aprobadas y
fallidas) y conservar la colección y el environment como entregables.

---

# 19. Analizar los fallos

No pedir inmediatamente:

```text
corrige todo
```

Primero solicitar:

```text
Analiza las pruebas que fallaron.

Para cada fallo indica:

- request y endpoint;
- nombre de la aserción que falló;
- causa;
- comportamiento actual;
- comportamiento esperado;
- capa donde probablemente está el problema;
- evidencia del resultado recibido por Postman.

No modifiques código todavía.
```

Luego los estudiantes deben decidir qué corregir.

---

# 20. Flujo completo de trabajo

El proceso utilizado en la práctica será:

```text
REQUERIMIENTO
      ↓
    SKILLS
      ↓
 IMPLEMENTACIÓN
      ↓
 ┌──────────────┐
 │  ARCHITECT   │
 │   revisa     │
 └──────┬───────┘
        ↓
   CORRECCIONES
        ↓
 ┌──────────────┐
 │    TESTER    │
 │ diseña tests │
 └──────┬───────┘
        ↓
 POSTMAN RUNNER
        ↓
   RESULTADOS
        ↓
 VALIDACIÓN HUMANA
```

---

# 21. Diferencia entre Skill y Agent

Al finalizar, el estudiante debe poder explicar:

```text
SKILL
```

Contiene conocimiento.

Ejemplo:

```text
Una arquitectura por capas debe utilizar:

Controller
Service
Repository
```

Mientras que:

```text
AGENT
```

Tiene una responsabilidad.

Ejemplo:

```text
Architect:

"Voy a revisar si el proyecto
cumple la arquitectura."
```

Otro ejemplo:

```text
Testing Skill:

"Una colección Postman debe validar
los endpoints con casos exitosos,
errores y casos límite."
```

Mientras que:

```text
Tester Agent:

"Voy a analizar esta API,
definir sus casos de prueba
y ejecutar las pruebas."
```

---

# 22. Actividad de cierre

Cada grupo debe entregar:

1. Código fuente de la API.
2. Carpeta `app/mappers/` con los mappers utilizados.
3. Skills utilizadas.
4. Agente `architect`.
5. Agente `tester`.
6. Modelo de relaciones.
7. Reporte inicial del Architect.
8. Correcciones realizadas a partir del reporte.
9. Matriz de pruebas propuesta por Tester.
10. Colección Postman `postman/UsersApi.postman_collection.json`.
11. Environment `postman/Local.postman_environment.json` sin secretos.
12. Resultado de ejecución del Collection Runner o Newman.
13. Pruebas unitarias de mappers con pytest, si fueron requeridas.
14. Al menos dos casos límite identificados.
15. Explicación de un error cometido por la IA y cómo fue detectado.

---

# 23. Preguntas de reflexión

Responder:

```text
1. ¿Qué diferencia existe entre un prompt y una Skill?

2. ¿Qué diferencia existe entre una Skill y un Agent?

3. ¿Por qué el agente Architect no debería encargarse
   también de implementar toda la aplicación?

4. ¿Qué principio SOLID se relaciona con esa separación?

5. ¿Una aplicación que funciona necesariamente
   tiene una buena arquitectura?

6. ¿Qué responsabilidad tiene un mapper y qué responsabilidades no debe asumir?

7. ¿Por qué es importante probar casos límite?

8. ¿Por qué no debemos aceptar automáticamente
   las correcciones propuestas por la IA?
```

---

# Idea central de la práctica

```text
CONOCIMIENTO DEL ESTUDIANTE
          ↓
        SKILLS
          ↓
       OPENCODE
          ↓
         CÓDIGO
          ↓
   AGENTES ESPECIALIZADOS
      ↙             ↘
 ARCHITECT         TESTER
      ↘             ↙
       VALIDACIÓN
          ↓
      ESTUDIANTE
```

La IA genera y analiza código, pero el estudiante sigue siendo responsable de comprender, verificar y aceptar las decisiones de ingeniería.
