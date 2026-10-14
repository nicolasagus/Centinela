---
name: docker-ephemeral-sandbox
description: Ejecuta tests en contenedores Docker efímeros con límites.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [docker, sandbox, ephemeral, testing, isolation]
    related_skills: [sdd-tdd-pipeline, systematic-debugging, safe-dev-lifecycle, docker-env-troubleshooter]
---

# Docker Ephemeral Sandbox

## Overview

Ejecución de suites de prueba aisladas dentro de contenedores efímeros Docker (`--rm`) con límites estrictos de hardware.

**Core principle:** Nunca compilar ni ejecutar tests en el host — siempre en contenedores efímeros con recursos acotados.

## When to Use

Usar siempre que se requiera compilar, correr tests (pytest, vitest, jest) o ejecutar scripts sin comprometer el host del sistema.

**Usar ESPECIALLY cuando:**
- Se ejecutan tests de terceros o no confiables
- Se compilan dependencias con posibles conflictos de versión
- Se necesita reproducir un entorno limpio y determinista
- Se corre código con consumo de recursos desconocido
- Se integra con CI/CD que exige aislamiento

**No usar cuando:**
- Se requiere interactividad con el host (pantalla, GPU dedicada)
- El proyecto no usa Docker y no puede empaquetarse
- El overhead de construir el contenedor supera ampliamente el beneficio

## Reglas Obligatorias:
1. Uso obligatorio de `--rm` y límites estrictos de recursos: `--memory="1g" --cpus="2"`.
2. Montaje del workspace del proyecto en `/workspace` dentro del contenedor.
3. Soporte para Python (`python:3.11-slim`) ejecutando `pytest -q`.
4. Soporte para Node/TS (`node:20-alpine`) ejecutando `npx vitest run`.
5. Capturar stdout, stderr y exit code; abortar ante timeouts (> 45s).

## Quick Commands

### Python

```bash
docker run --rm --memory="1g" --cpus="2" -v "$PWD":/workspace -w /workspace python:3.11-slim pytest -q
```

### Node/TypeScript

```bash
docker run --rm --memory="1g" --cpus="2" -v "$PWD":/workspace -w /workspace node:20-alpine npx vitest run
```

### Jest (Node)

```bash
docker run --rm --memory="1g" --cpus="2" -v "$PWD":/workspace -w /workspace node:20-alpine npx jest --coverage --verbose
```

## Timeout Handling

Cuando la ejecución supera los 45 segundos, abortar inmediatamente:

```bash
docker run --rm --memory="1g" --cpus="2" -v "$PWD":/workspace -w /workspace node:20-alpine timeout 45 npx vitest run
```

## Integration Notes

- Vincular fallos con `systematic-debugging` para investigar la causa raíz.
- Integrar con `sdd-tdd-pipeline` como fase de verificación obligatoria.
- Registrar stdout/stderr en archivos de artefacto para auditoría.