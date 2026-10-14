---
name: autonomous-task-orchestrator
description: Descompone requerimientos complejos en subtareas atómicas.
version: 1.0.0
author: Nicolas
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [planning, autonomy, task-decomposition, execution, agent]
    related_skills: [sdd-tdd-pipeline, safe-dev-lifecycle, token-frugal-coder, meta-prompt-engineer]
---

# Autonomous Task Orchestrator (Superpowers Protocol)

## Overview
Protocolo para operar en modo piloto automático: analiza proyectos de gran envergadura, los fragmenta en unidades atómicas de trabajo y los ejecuta secuencialmente sin perder el objetivo global.

## When to Use
- **Aplicar cuando:** El usuario solicite desarrollar un módulo completo, realizar una refactorización amplia o resolver requerimientos de múltiples pasos.
- **No aplicar cuando:** Sean tareas puntuales de una sola línea, consultas breves o ejecuciones de un único comando.

---

## Procedimiento Obligatorio

### 1. Descomposición Atómica (Fase de Planificación)
Antes de generar código:
1. Analizar el objetivo final y redactar un `PLAN.md` interno estructurado en fases numeradas (Paso 1, Paso 2, Paso 3).
2. Cada paso debe ser **atómico**: debe poder implementarse, compilarse y verificarse de forma independiente en menos de 5 minutos.
3. Definir claramente el criterio de aceptación (*Definition of Done*) para cada paso.

### 2. Ejecución con Checkpoints (Piloto Automático)
Para cada subtarea del plan:
1. **Enfoque único:** Concentrarse exclusivamente en la subtarea activa sin adelantar código de pasos posteriores.
2. **Implementación y Verificación:** Escribir el código y ejecutar sus pruebas inmediatamente en el sandbox.
3. **Validación:** Si el paso no pasa sus pruebas o no compila, invocar `systematic-debugging`. Prohibido avanzar al paso siguiente con errores pendientes.
4. **Checkpoint:** Marcar la subtarea como completada antes de transicionar a la siguiente.

### 3. Preservación del Estado Global
- Mantener un registro conciso del progreso: `[X/Total]` pasos completados.
- Si surge un imprevisto técnico o bloqueo arquitectónico durante un paso:
  - Detener la ejecución.
  - Ajustar el plan restante.
  - Registrar la decisión en `graph-memory-core` para no reincidir.

### 4. Consolidación Final
Al concluir todos los pasos:
- Ejecutar la suite completa de pruebas de regresión.
- Presentar un reporte final consolidado de hitos cumplidos y artefactos generados.