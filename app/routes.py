# =================================
#IMPORTS
# =================================
from dbm import error
from flask import jsonify, request
from .models import Task
from . import db
# =================================


# =================================
#VALIDACIONES
# =================================

def validate_create_task(data):
    if not data or "title" not in data:
        return "Falta el título"

    if not data["title"].strip():
        return "Título vacío"

    if len(data["title"]) > 100:
        return "Título demasiado largo"

    if "done" in data and not isinstance(data["done"], bool):
        return "El campo done debe ser booleano"

    return None


def validate_update_task(data):
    if "title" in data:
        if not data["title"].strip():
            return "Título vacío"

        if len(data["title"]) > 100:
            return "Título demasiado largo"

    if "done" in data and not isinstance(data["done"], bool):
        return "El campo done debe ser booleano"

    return None

# =================================
#ENDPOINTS
# =================================

def register_routes(app):

    #Ruta de prueba para comprobar que el servidor funciona
    @app.route("/")
    def home():
        return "Servidor funcionando"

    #Ruta GET para obtener todas las tareas
    @app.route("/tasks", methods= ["GET"])
    def get_tasks():

        query = Task.query

        # Filtro por estado (done)
        done = request.args.get("done")
        if done is not None:
            if done.lower() == "true":
                query = query.filter_by(done=True)
            elif done.lower() == "false":
                query = query.filter_by(done=False)
            else:
                return {"error": "El parámetro 'done' debe ser 'true' o 'false'"}, 400
            
        # Filtro por título (búsqueda parcial)
        title = request.args.get("title")
        if title:
            query = query.filter(Task.title.contains(title))

        tasks = query.all()

        return [task.to_dict() for task in tasks]
    
    
    #Ruta GET para obtener una tarea por su ID
    @app.route("/tasks/<int:task_id>")
    def get_task(task_id):

        task = Task.query.get(task_id)

        if not task:
             return {"error": "Tarea no encontrada"}, 404
        return jsonify(task.to_dict())
    
    #Ruta POST para crear una nueva tarea
    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.get_json()

        #Validación de los datos de entrada para el POST
        error = validate_create_task(data)
        if error:
            return {"error": error}, 400
        
        new_tasks = Task(
            title=data["title"],
            done=False,
            description=data.get("description")
        )


        db.session.add(new_tasks)
        db.session.commit()
        
        return jsonify(new_tasks.to_dict()), 201
    
    #Ruta DELETE para eliminar una tarea por su ID
    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        #Comprobamos si la tarea existe antes de intentar borrarla
        task = Task.query.get(task_id)
        
        if not task:
            return {"error": "Tarea no encontrada"},404
        
        db.session.delete(task)
        db.session.commit()
            
        return {"message": "Tarea eliminada"}
    
    #Ruta PUT para actualizar una tarea por su ID
    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):

        #Comprobamos si la tarea existe antes de intentar actualizarla
        task = Task.query.get(task_id)
        if not task:
            return {"error": "Tarea no encontrada"}, 404

        
        data = request.get_json()

        #Validación de los datos de entrada para el UPDATE
        error = validate_update_task(data)
        if error:
            return {"error": error}, 400

        if "done" in data and not isinstance(data["done"], bool):
            return {"error": "El campo 'done' debe ser un valor booleano"}, 400

        if not data:
            return {"error": "No JSON provided"},400
        
        task.title = data.get("title", task.title)
        task.done = data.get("done", task.done)
        task.description = data.get("description", task.description)

        db.session.commit()

        return jsonify(task.to_dict())
