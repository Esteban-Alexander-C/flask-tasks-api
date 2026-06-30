from app.validators import validate_update_task, validate_delete_task, validate_create_task

#Update Test
def test_validate_update_task():
    
    assert validate_update_task({"done": "hola"}) == "El campo 'done' debe ser un valor booleano"

def test_validate_update_task_empty():
    assert validate_update_task({}) == "No se han enviado datos"

def test_validate_update_task_ok():
    assert validate_update_task({"done": True}) == None

#Create Test
def test_validate_create_task():

    assert validate_create_task({"title": ""}) == "El título es obligatorio"
#Delete Test                                
def test_validate_delete_task_ok():

    assert validate_delete_task({"id": 4}) == None

def test_validate_delete_task_not_int():

    assert validate_delete_task({"id": "hola"}) == "El ID de la tarea debe ser un número entero"

def test_validate_delete_task_empty():

    assert validate_delete_task({}) == "No se han enviado datos"