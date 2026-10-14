---
name: sdd-tdd-pipeline
description: SDD+TDD pipeline con ejecución de tests en Docker efímero.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [engineering, sdd, tdd, docker, pipeline]
    related_skills: [systematic-debugging, test-driven-development, subagent-driven-development, docker-ephemeral-sandbox, safe-dev-lifecycle, autonomous-task-orchestrator]
---

# SDD + TDD Pipeline

## Overview

Desarrollo Spec-Driven (SDD) combinado con Test-Driven (TDD), con aislamiento obligatorio en contenedores Docker efímeros.

**Core principle:** NO hay implementación sin spec aprobada y sin tests pasando en verde.

## When to Use

Usar para cualquier tarea de desarrollo de software que requiera:
- Estructura rigurosa de especificación antes de código
- Cobertura completa de tests unitarios e integración
- Ejecución aislada reproducible en contenedores Docker

**Usar ESPECIALLY cuando:**
- El proyecto tiene múltiples módulos o equipos
- Se requiere auditoría de decisiones de diseño
- La calidad y trazabilidad son prioritarias sobre velocidad
- Se integran dependencias externas que pueden fallar

**No usar cuando:**
- Es un prototipo desechable (< 1 hora de esfuerzo)
- El scope es trivial (una sola función sin dependencias)
- No hay acceso a Docker o recursos para contenedores

## Reglas Obligatorias:
1. Diseñar tipos, interfaces y excepciones antes de codificar la lógica.
2. Escribir pruebas unitarias e integración completas (Vitest/Jest para TS, Pytest para Python).
3. Ejecutar los tests obligatoriamente dentro de contenedores Docker efímeros ('node:20-alpine' o 'python:3.11-slim').
4. Si los tests fallan (exit code != 0), usar 'systematic-debugging' para corregir la implementación hasta que todos los tests pasen en verde.
5. Estructurar la entrega final en: spec.md, tests/, src/ y reporte_auditoria.md.

## Integration

- Vincular con `docker-ephemeral-sandbox` para la ejecución de contenedores.
- La fase de verificación de tests es obligatoria en cada iteración del pipeline.

## Related

- [docker-ephemeral-sandbox](./docker-ephemeral-sandbox/SKILL.md)
- [systematic-debugging](./systematic-debugging/SKILL.md)
- [test-driven-development](./test-driven-development/SKILL.md)
- [subagent-driven-development](./subagent-driven-development/SKILL.md)

## Quick Reference

| Fase | Entregable | Verificación |
|------|-----------|--------------|
| 1. Spec | spec.md con tipos, interfaces, excepciones | Revisión de diseño |
| 2. Tests | tests/ con unitarios e integración | Tests verdes en Docker |
| 3. Code | src/ con implementación mínima | Tests siguen pasando |
| 4. Report | reporte_auditoria.md | Trazabilidad completa |
| 5. Clean | Refactorización | Tests aún verdes |

## Docker Commands

### Python
```bash
docker run --rm --memory="1g" --cpus="2" -v "$PWD":/workspace -w /workspace python:3.11-slim pytest -q
```

### Node/TS
```bash
docker run --rm --memory="1g" --cpus="2" -v "$PWD":/workspace -w /workspace node:20-alpine npx vitest run
```

## Failure Protocol

1. Tests fallan → ejecutar systematic-debugging
2. Investigar root cause (Phase 1-2)
3. Corregir implementación (Phase 3-4)
4. Re-ejecutar tests en Docker (confirmar fix)
5. Documentar hallazgos en reporte_auditoria.md

## Real-World Impact

- Tests aislados: cero efectos laterales entre ejecuciones
- Límites de hardware: contenedores nunca consumen más del especificado
- Auditoría completa: spec → tests → código → reporte trazable
- Debugging sistemático: cada fallo se resuelve con método, no con guessing

**No hay atajos. Spec primero. Tests verdes. Docker siempre.**
