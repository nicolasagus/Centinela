---
name: token-frugal-coder
description: Protocolo de economía de contexto y respuestas técnicas.
version: 1.0.0
author: Nicolas
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [performance, tokens, optimization, context-window, efficiency]
    related_skills: [safe-dev-lifecycle, systematic-debugging, autonomous-task-orchestrator, meta-prompt-engineer]
---

# Token-Frugal Engineering Protocol

## Overview
Directiva operativa para maximizar la ventana de contexto útil reduciendo drásticamente la verbosidad, el volcado de logs masivos y la lectura completa de archivos innecesarios.

## When to Use
- **Aplicar cuando:** El agente realice tareas de desarrollo, depuración, lectura de código, ejecución de comandos o generación de respuestas técnicas.
- **No aplicar cuando:** El usuario solicite explícitamente tutoriales extensos, guías paso a paso para principiantes o explicaciones teóricas detalladas.

---

## Reglas Obligatorias de Economía de Tokens

### 1. Inspección Quirúrgica (Prohibido leer archivos enteros)
- Antes de leer un archivo con más de 100 líneas, localizar la sección objetivo usando `search_files` con patrones regex o búsqueda de símbolos.
- Usar lectura por rangos de líneas (offset/limit) en lugar de volcar el archivo completo al contexto.
- Para entender la estructura de carpetas, usar `tree` limitado a nivel 2 o listas de archivos específicas; nunca inspeccionar directorios recursivos sin filtro.

### 2. Contención de Salida de Herramientas y Logs
- Prohibido ejecutar comandos que escupan miles de líneas a la consola.
- Al consultar logs o pruebas, restringir la salida:
  - Usar flags silenciosos: `pytest -q`, `npm test -- --silent`, `docker logs --tail 50`.
  - Si un comando falla, aislar únicamente el stack trace relevante; no reenviar la salida completa anterior al error.

### 3. Modificaciones sin Repetición de Código (*Diff Mentality*)
- Al proponer o aplicar cambios en archivos existentes:
  - No reescribir archivos enteros en el mensaje final.
  - Generar diffs unificados o aplicar reemplazos directos sobre la función o bloque afectado.

### 4. Cero Relleno Conversacional (*No Fluff*)
- Omitir introducciones amables ("¡Claro! Con gusto te ayudo con esto..."), resúmenes obvios o conclusiones redundantes.
- Responder directamente con el resultado de la acción, la salida del test y la lista precisa de archivos modificados.
- Explicar la causa raíz de un bug en un máximo de 2 oraciones técnicas.