# 🕹️ Guía Operativa: Control de Entorno Zensical (Docker)

Este documento centraliza los comandos necesarios para gestionar el ciclo de vida del contenedor de documentación de **Self Service - Courses**, utilizando la configuración personalizada de este repositorio.

## 📋 Información de Configuración
* **Archivo de Orquestación:** `docker_compose_gblog_start.yml`
* **Nombre del Contenedor:** `Dockerfile`
* **Imagen Base:** `python:3.11-slim` (con Zensical preinstalado)
* **Puerto de Acceso:** `47829`

---

## 🚀 1. Iniciar y Construir el Entorno
Para arrancar el servidor de desarrollo por primera vez o después de modificar el `Dockerfile`:

```bash
# Construye la imagen y levanta el servicio en segundo plano (detached)
docker compose -f docker_compose_gblog_start.yml up -d --build
````

```bash
# Detiene la ejecución pero mantiene el contenedor creado
docker compose -f docker_compose_gblog_start.yml stop
```

```bash
# Baja el entorno y elimina imágenes asociadas y volúmenes
docker compose -f docker_compose_gblog_start.yml down --rmi all --volumes
```

```bash
# Ver los logs del contenedor en tiempo real
docker logs -f docker_compose_gblog_start.yml

# Listar el estado del contenedor para verificar si está corriendo (Up)
docker ps -a --filter "docker_compose_gblog_start"
```