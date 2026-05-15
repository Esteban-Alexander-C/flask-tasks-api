Tareas Flask API 

API REST desarrollada con Flask para gestionar tareas (tasks) mediante operaciones CRUD


DESCRIPCION

Este proyecto consiste en una API REST que actúa como intermediario entre un cliente (navegador o herramientas como Thunder Client) y una base de datos

El cliente envía peticiones HTTP para crear, consultar, actualizar o eliminar tareas. Flask recibe estas peticiones a través de distintos endpoints, ejecuta la lógica correspondiente y utiliza SQLAlchemy para interactuar con una base de datos SQLite.

Finalmente, el servidor devuelve respuestas en formatos JSON.

El proyecto sigue el patrón Application Factory, lo que permite una mejor organización y escalibidad del código.

TECNOLOGIAS UTILIZADOS

-Python 
-Flask
-SQLAlchemy
-SQLite
-JSON //Quitar

ENDPOINTS

-GET (/tasks) -->Obtener todas las tareas
-GET (/tasks/'id') --> Obtener una tarea específica
-POST (/tasks) --> Crear una tarea 
-PUT (/tasks/'id') --> Actualizar una tarea
-DELETE (/tasks/'id') --> Eliminar una tarea

INSTALACIÓN Y USO 

1. Clonar repositorio:

git clone https://github.com/Kayzza/flask-tasks-api.git 
cd flask-tasks-api

2. Crear entorno virtual:

python -m venv .venv

3. Activar entorno:

.venv\Scripts\activate

4. Instalar dependencias:

pip install flask flask-sqlalchemy

5. Ejectuar la aplicación:

python run.py

CONOCIMIENTOS APLICADOS

-API REST
-CRUD
-Arquitectura Application Factory
-ORM(SQLAlchemy)
-Manejo de peticiones HTTP

ESTADO DEL PROYECTO(15/05)

Proyecto funcional con operaciones CRUD completas
Pendiente de mejoras como validaciones, filtros y documentación más avanzada

