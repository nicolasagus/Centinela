---
name: safe-dev-lifecycle
description: Protocolo seguro para modificar código con Git y tests.
version: 1.0.0
author: Nicolas
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [engineering, git, quality, testing, clean-code]
    related_skills: [sdd-tdd-pipeline, docker-ephemeral-sandbox, systematic-debugging, docker-env-troubleshooter, graph-memory-core, token-frugal-coder, autonomous-task-orchestrator]
---

# Protocolo Seguro de Desarrollo y Modificación de Proyectos

## Overview
Procedimiento operativo estándar para intervenir repositorios de software minimizando riesgos de regresión, fugas de secretos y contaminación de ramas Git.

## When to Use
- **Aplicar cuando:** El usuario solicite implementar features, refactorizar, resolver bugs o ejecutar tareas directas sobre el código base de un repositorio.
- **No aplicar cuando:** El usuario haga consultas conceptuales, pida explicaciones teóricas o solicite snippets aislados sin contexto de repositorio.

---

## Procedimiento Obligatorio

### 1. Fase de Inspección y Contexto (Solo Lectura)
Antes de modificar cualquier archivo:
- Identificar estructura del proyecto (`package.json`, `docker-compose.yml`, `.csproj`, `requirements.txt`, etc.).
- Revisar estado de Git (`git status`, `git branch`).
- **Prohibido:** Modificar código sin haber leído el archivo objetivo completo y sus dependencias directas.

### 2. Fase de Ejecución y Cambios Quirúrgicos
- Realizar únicamente los cambios necesarios para cumplir el requerimiento.
- Respetar patrones de diseño, convenciones de nomenclatura y estilo del repositorio.
- **Preservación:** No eliminar código preexistente salvo solicitud explícita o refactorización consensuada.
- **Seguridad:** Prohibido escribir secretos, API keys o tokens hardcodeados. Validar que `.env` figure en `.gitignore`.

### 3. Fase de Verificación y Compilación
Antes de dar la tarea por concluida:
1. **Linter / Compilación:** Ejecutar build o verificación estática (`npm run build`, `tsc --noEmit`, `dotnet build`).
2. **Tests:** Correr la suite de pruebas mediante `docker-ephemeral-sandbox` o runner local configurado.
3. Si la verificación falla:
   - Diagnosticar el error aplicando `systematic-debugging`.
   - Subsanar la causa raíz.
   - Reejecutar hasta obtener salida limpia (exit code 0).

### 4. Fase de Cierre y Control de Versiones
- Ejecutar `git diff --stat` para auditar la superficie de cambios.
- Si se requiere ramificación o commit:
  - Crear rama dedicada: `feature/<nombre>` o `fix/<nombre>`.
  - Aplicar formato Conventional Commits (ej. `feat(auth): add token validation`).
  - **Higiene:** Verificar que `git status` no contenga artefactos compilados (`node_modules/`, `bin/`, `obj/`, `dist/`, `.env`).

### 5. Resumen de Entrega
Reportar al usuario:
- Archivos creados o modificados.
- Salida del build y resultado de la suite de pruebas.
- Estado de la rama y sugerencias operativas inmediatas.
