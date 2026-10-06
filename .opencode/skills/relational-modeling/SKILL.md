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