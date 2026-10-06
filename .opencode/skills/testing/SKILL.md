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