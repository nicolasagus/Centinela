**# Centinela v0.1**



**Motor autónomo de ingeniería de software con bucle cerrado (FSM), TDD estricto y ejecución aislada en Docker efímero con control de recursos cgroups.**



**## Características de v0.1**

**- \*\*Freno Cognitivo Visual:\*\* Modelado de diagramas en ASCII y Mermaid previo a la codificación.**

**- \*\*Aislamiento en Docker:\*\* Ejecución de pruebas en contenedores Alpine con límites estrictos (--memory="1g" --cpus="2").**

**- \*\*TDD y Self-Healing:\*\* Suite de pruebas automatizada con autorreparación determinista (42/42 tests validados).**

**- \*\*Gobernanza de Host:\*\* Entorno local bajo WSL2 restringido a 6 GB de RAM.
## Fase 2: Gobernanza Determinista y Memoria por Grafos (v0.2-dev)**



**- \*\*Strict Schema Enforcement:\*\* Todas las respuestas de transición de estado se rigen formalmente por `core/guards/response-grammar.json` (Draft-07), erradicando texto conversacional no estructurado.**

**- \*\*Circuit Breaker:\*\* Monitoreo y límite rígido de 3 iteraciones de autoreparación y 16.384 tokens máximos de contexto (`core/guards/circuit-breaker.config.json`).**

**- \*\*Graph-RAG Memory (Dijkstra):\*\* Navegación determinista de árboles de dependencias y podado de contexto mediante camino mínimo (`core/memory/graph-navigator.py`).**

