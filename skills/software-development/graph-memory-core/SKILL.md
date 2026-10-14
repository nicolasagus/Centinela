---
name: graph-memory-core
description: Memoria en grafo para arquitectura, decisiones y bugs.
version: 1.0.0
author: Nicolas
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [memory, graph, rag, persistence, knowledge-base]
    related_skills: [safe-dev-lifecycle, systematic-debugging]
---

# Knowledge Graph Memory System

## Overview
Sistema de memoria asociativa en grafo para recordar patrones de repositorios, contratos de clases, decisiones arquitectónicas y soluciones a errores recurrentes con costo mínimo de tokens.

## When to Use
- **Aplicar cuando:** Se identifique una regla de arquitectura clave, una relación entre módulos, o la causa y solución de un bug difícil que deba recordarse a futuro.
- **No aplicar cuando:** Sean logs efímeros, variables temporales o código desechable sin relevancia futura.

---

## Procedimiento Obligatorio

### 1. Modelo de Datos del Grafo
El grafo se persiste localmente en `.hermes/memory/graph.json` con la siguiente estructura de tripletas:
- **Entidades (Nodos):** `{ id, label, type, metadata }`
  - Tipos válidos: `Module`, `Class`, `Function`, `Bug`, `Rule`, `Dependency`.
- **Relaciones (Aristas):** `{ source, target, relation, context }`
  - Relaciones estándar: `DEPENDS_ON`, `IMPLEMENTS`, `RESOLVED_BY`, `CALLS`, `VIOLATES`.

### 2. Fase de Ingesta (Añadir Conocimiento)
Al finalizar una tarea o resolver un error con `systematic-debugging`:
- Extraer las tripletas esenciales del cambio.
- Si se resolvió un bug crítico:
  - Crear nodo `Bug: <NombreError>`.
  - Crear arista `[Bug] -> (RESOLVED_BY) -> [Solución/Técnica]`.
- Actualizar el grafo local sin duplicar nodos existentes.

### 3. Fase de Recuperación Quirúrgica (Query)
Antes de planificar una refactorización o cambio sobre un módulo:
- Consultar los nodos vecinos del módulo objetivo a una profundidad máxima de 1 o 2 saltos.
- Inyectar únicamente las relaciones relevantes al prompt activo (evitando volcar el grafo completo).

### 4. Higiene y Consistencia
- No almacenar bloques de código completos; registrar firmas, nombres de métodos y directivas.
- Si una entidad queda obsoleta tras una refactorización, actualizar o eliminar la relación correspondiente.