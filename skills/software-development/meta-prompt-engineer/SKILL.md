---
name: meta-prompt-engineer
description: Diseño de prompts estructurados para delegar a otros LLMs.
version: 1.0.0
author: Nicolas
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [prompt-engineering, metaprompting, llm, orchestration, system-prompts]
    related_skills: [token-frugal-coder, autonomous-task-orchestrator]
---

# Meta-Prompt Engineering Protocol

## Overview
Protocolo para formular instrucciones estructuradas, system prompts y tareas de delegación dirigidas a otros modelos de lenguaje (como Gemini, Claude u otros subagentes locales) maximizando determinismo y reduciendo alucinaciones.

## When to Use
- **Aplicar cuando:** Se requiera formular un prompt de auditoría, generar directivas para un subagente, redactar contratos de interfaz para un LLM externo o crear plantillas de entrada/salida.
- **No aplicar cuando:** Se interactúe directamente con el usuario en respuestas de chat convencionales.

---

## Reglas Obligatorias de Diseño de Prompts

### 1. Delimitación Estricta por Etiquetas Semánticas (XML Tags)
- Separar siempre el contexto de la instrucción mediante etiquetas claras:
  `<role>`, `<task>`, `<context>`, `<constraints>`, `<output_format>`.
- Aislar el código fuente o los datos a analizar dentro de `<source_code>` o `<input_data>` para evitar ataques de inyección indirecta o confusiones semánticas.

### 2. Definición Negativa y Casos Borde (<constraints>)
- Todo prompt generado debe contener restricciones explícitas de lo que **NO** debe hacer el modelo:
  - "No incluir código boilerplate redundante."
  - "No inventar dependencias fuera del listado provisto."
  - "Prohibido omitir el manejo de excepciones tipadas."

### 3. Contrato de Salida Rígido (<output_format>)
- Exigir un formato estructurado y parseable (JSON puro, diff unificado, o bloque Markdown específico).
- En salidas JSON, indicar explícitamente: "Responde estrictamente con el bloque JSON sin texto introductorio ni formato conversacional."

### 4. Técnica Few-Shot / Ejemplos Sintéticos
- Si la tarea implica clasificación o análisis complejo, inyectar exactamente un ejemplo mínimo de entrada y salida esperada dentro de `<example>`.