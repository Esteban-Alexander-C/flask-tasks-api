
def test_get_task(client):

    response = client.get("/tasks") 

    assert response.status_code == 200
    data = response.get_json()

    assert data["tasks"] == []

def test_get_task_by_id(client):
    create = client.post("/tasks", json={"title": "Test"})
    task = create.get_json()

    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    data = response.get_json()

    assert data["id"] == task["id"]

def test_get_task_not_found(client):
    response = client.get("/tasks/999")

    assert response.status_code == 404

def test_create_task(client):
    response = client.post("/tasks", json={
    "title": "Nueva tarea"
    })

    assert response.status_code == 201

    data = response.get_json()
    assert data["title"] == "Nueva tarea"

def test_create_task_invalid(client):
    
    response = client.post("/tasks", json={
    "title": ""
    })
    assert response.status_code == 400

def test_update_task_endpoint(client):
    
    create = client.post("/tasks", json={"title": "Viejo"})
    task = create.get_json()

    response = client.put(f"/tasks/{task['id']}", json={
        "title": "Nuevo"
    })

    assert response.status_code == 200
    data = response.get_json()

    assert data["title"] == "Nuevo"

def test_delete_task_endpoint(client):
    create = client.post("/tasks", json={"title": "Eliminar"})
    task = create.get_json()

    response = client.delete(f"/tasks/{task['id']}")

    assert response.status_code == 200