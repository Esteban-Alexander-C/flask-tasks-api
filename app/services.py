from .models import Task
from . import db

def get_tasks_service(done=None, title=None, sort= None, page=1, per_page=5):
    query = Task.query

    #----- FILTROS -----
    if done is not None:
        query = query.filter_by(done=done)

    if title:
        query = query.filter(Task.title.contains(title))

    #----- ORDENACIÓN -----
    if sort:
        if sort.startswith("-"):
            field = sort[1:]
            if field == "title":
                query = query.order_by(Task.title.desc())
            elif field == "id":
                query = query.order_by(Task.id.desc())
        else:
            if sort == "title":
                query = query.order_by(Task.title.asc())
            elif sort == "id":
                query = query.order_by(Task.id.asc())

    #----- PAGINACIÓN -----
    return query.paginate(page=page, per_page=per_page, error_out=False)

#Servicio para crear una nueva tarea
def create_task_service(data):
    #Creamos un objeto de la clase Task con los datos proporcionados
    new_task = Task(
        title=data["title"],
        done=False,
        description=data.get("description")
    )
    #Guardamos la nueva tarea en la base de datos
    db.session.add(new_task)
    db.session.commit()
    #Devolvemos la nueva tarea creada
    return new_task

#Servicio para actualizar una tarea existente
def update_task_service(task_id, data):
    task = Task.query.get(task_id)

    if not task:
        return None

    if "title" in data:
        task.title = data["title"]

    if "done" in data:
        task.done = data["done"]

    if "description" in data:
        task.description = data["description"]

    db.session.commit()

    return task

#Servicio para eliminar una tarea existente
def delete_task_service(task_id):
    task = Task.query.get(task_id)

    if not task:
        return None
    
    db.session.delete(task)
    db.session.commit()
    
    return task