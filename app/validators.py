def validate_create_task(data): 
    if not data:
        return "No se han enviado datos"
    
    if 'title' not in data or not data['title']:
        return "El título es obligatorio"
    
    if 'done' in data and not isinstance(data['done'], bool):
        return "El campo 'done' debe ser un valor booleano"
    
    if 'description' in data and not isinstance(data['description'], str):
        return "El campo 'description' debe ser una cadena de texto"
    
    if len(data["title"]) > 100:
        return "Título demasiado largo"
    
    return None

def validate_update_task(data):
    
    if not data:
        return "No se han enviado datos"
    
    if "title" in data and not data["title"]:
            return "Título no puede estar vacío"

    if "done" in data and not isinstance(data["done"], bool):
        return "El campo 'done' debe ser un valor booleano"
    
    if "description" in data and not isinstance(data["description"], str):
        return "El campo 'description' debe ser una cadena de texto"

    return None

def validate_delete_task(task_id):
    if not isinstance(task_id, int):
        return "El ID de la tarea debe ser un número entero"
    return None