# =================================
#IMPORTS
# =================================
from dbm import error
from flask import jsonify, request
from .models import Task
from . import db
from .services import create_task_service, get_tasks_service, update_task_service, delete_task_service
from .validators import validate_create_task, validate_update_task, validate_delete_task

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

        # -----LEER PARÁMETROS -----
        done = request.args.get("done")
        title = request.args.get("title")
        sort = request.args.get("sort")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        # ----- VALIDACIÓN -----
        if done is not None:
            if done.lower() == "true":
                done = True
            elif done.lower() == "false":
                done = False
            else:
                return {"error": "El parámetro 'done' debe ser 'true' o 'false'"}, 400
            
        # ----- LLAMADA AL SERVICIO -----
        paginated_tasks = get_tasks_service(done, title, sort, page, per_page)

        # ----- RESPUESTA -----
        return {
            "total": paginated_tasks.total,
            "page": paginated_tasks.pages,
            "current_page": page,
            "tasks": [task.to_dict() for task in paginated_tasks.items]
        }
        
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

        #Validación
        error = validate_create_task(data)
        if error:
            return {"error": error}, 400
        
        #Lógica en services.py
        new_task = create_task_service(data)

        return new_task.to_dict(), 201

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
        
        deleted_task = delete_task_service(task_id)

        if not deleted_task:
            return {"error": "Tarea no encontrada"}, 404
            
        return {"message": "Tarea eliminada correctamente"}, 200
    
    #Ruta PUT para actualizar una tarea por su ID
    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        data = request.get_json()

        #Validación 
        error = validate_update_task(data)
        if error:
            return {"error": error}, 400
        
        #Lógica
        updated_task = update_task_service(task_id, data)

        if not updated_task:
            return {"error": "Tarea no encontrada"}, 404

        return updated_task.to_dict(), 200
