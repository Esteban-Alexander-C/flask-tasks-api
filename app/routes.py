from flask import jsonify, request
from .models import Task
from . import db
#Simulamos base de datos en memoria 


def register_routes(app):

    @app.route("/")
    def home():
        return "Servidor funcionando"

    @app.route("/tasks", methods= ["GET"])
    def get_tasks():

        tasks = Task.query.all()

        return jsonify([task.to_dict() for task in tasks])
    
    #Para recoger una tarea con un id especifico
    @app.route("/tasks/<int:task_id>")
    def get_task(task_id):

        task = Task.query.get(task_id)

        if not task:
             return {"error": "Tarea no encontrada"}, 404
        return jsonify(task.to_dict())
    #Ruta POST para añadir tareas
    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.get_json()

        if not data or "title" not in data:
            return {"error":"Falta el título"}, 400
        
        new_tasks = Task(
            title=data["title"],
            done=False
        )


        db.session.add(new_tasks)
        db.session.commit()
        
        return jsonify(new_tasks.to_dict()), 201
    
    #Ruta DELETE para borrar tareas
    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):

        task = Task.query.get(task_id)

        if not task:
            return {"error": "Tarea no encontrada"},404
        
        db.session.delete(task)
        db.session.commit()
            
        return {"message": "Tarea eliminada"}
    
    #Ruta PUT para actualizar tareas
    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):

        task = Task.query.get(task_id)

        if not task:
                return {"error": "Tarea no encontrada"}, 404
        
        data = request.get_json()

        if not data:
            return {"error": "No JSON provided"},400
        
        task.title = data.get("title", task.title)
        task.done = data.get("done", task.done)

        db.session.commit()

        return jsonify(task.to_dict())