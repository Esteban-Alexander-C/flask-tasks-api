from app.services import create_task_service, update_task_service, delete_task_service, get_tasks_service
from app.models import Task

def test_create_task(app):
    data = {
        "title": "Nueva tarea",
        "description": "Descripción de la nueva tarea"
    }

    task = create_task_service(data)

    assert task.id is not None
    assert task.title == data["title"]
    assert task.done == False

def test_update_task(app):
    # Creamos una tarea de prueba
    task = create_task_service({"title": "Tarea de prueba"})

    updated = update_task_service(task.id, {"title": "Tarea actualizada"})

    assert updated.title == "Tarea actualizada"

def test_delete_task(app):
    task = create_task_service({"title": "Tarea a eliminar"})

    deleted = delete_task_service(task.id)

    assert deleted.id == task.id


def test_update_task_not_found(app):
    # Intentamos actualizar una tarea que no existe
    result = update_task_service(999, {"title": "Hola"})

    assert result is None

def test_delete_task_not_found(app):
    # Intentamos eliminar una tarea que no existe
    result = delete_task_service(999)

    assert result is None

def test_get_tasks_filter_done(app):
    # Creamos tareas de prueba
    create_task_service({"title": "Tarea 1"})
    t2 = create_task_service({"title": "Tarea 2"})

    # Marcamos la segunda tarea como completada
    t2.done = True
    from app import db
    db.session.commit()
    # Obtenemos las tareas filtradas por done=True
    result = get_tasks_service(done=True)

    assert len(result.items) == 1
    assert result.items[0].title == "Tarea 2"