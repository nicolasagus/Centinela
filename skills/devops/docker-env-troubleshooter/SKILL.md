---
name: docker-env-troubleshooter
description: Diagnóstico de entornos Docker, puertos y resolución.
version: 1.0.0
author: Nicolas
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [devops, docker, troubleshooting, containers, ports]
    related_skills: [docker-ephemeral-sandbox, safe-dev-lifecycle]
---

# Procedimiento de Diagnóstico y Gestión de Contenedores

## Overview
Protocolo operativo para diagnosticar, reiniciar, depurar y verificar servicios en Docker o entornos de red locales sin riesgo de pérdida de datos ni colisiones de puertos.

## When to Use
- **Aplicar cuando:** Se requiera levantar servicios con Docker, depurar contenedores en estado `Exited`, diagnosticar puertos ocupados o auditar logs de servicios caídos.
- **No aplicar cuando:** Solo se requiera ejecutar pruebas efímeras dentro de un sandbox temporal (usar `docker-ephemeral-sandbox`).

---

## Procedimiento Obligatorio

### 1. Verificación Previa de Puertos y Procesos
Antes de ejecutar `docker compose up` o levantar servicios expuestos:
- Comprobar disponibilidad de puerto en el host anfitrión:
  - En Windows: `netstat -ano | findstr :<puerto>`
  - En Linux/macOS: `lsof -i :<puerto>` o `ss -tulpn | grep :<puerto>`
- Si el puerto está tomado, identificar e informar el PID o contenedor causante antes de intentar el arranque.

### 2. Inspección Quirúrgica de Contenedores
Cuando un servicio falle o no responda:
1. Inspeccionar estados con `docker ps -a` identificando códigos de salida anormales (`Exit 137`, `Exit 1`, etc.).
2. Restringir la captura de logs para preservar la ventana de contexto:
   `docker logs --tail 100 <container_name_or_id>`
3. Revisar discrepancias de montaje de volúmenes o variables de entorno no resueltas.

### 3. Preservación Estricta de Persistencia
- **Prohibición crítica:** No ejecutar de forma autónoma `docker system prune -a` ni `docker volume prune -f`. Pueden destruir bases de datos locales, volúmenes de desarrollo e imágenes cacheadas.
- Para reiniciar o reconstruir servicios preservando volúmenes:
  `docker compose down && docker compose up -d --build`

### 4. Reporte de Diagnóstico y Acción
Al identificar la anomalía:
- Resumir la causa raíz en 2 líneas concretas.
- Proveer el comando correctivo exacto y verificar el restablecimiento del servicio con `docker ps`.