const API_URL = "http://127.0.0.1:5000/tasks";  //Endpoint del backend

//Cargo las tareas deesde el backend y las muestro en la lista
async function loadTasks() {
    const response = await fetch(API_URL); //Uso fetch para hacer un GET al endpoint 
    const data = await response.json(); //Convierto la respuesta a JSON

    const list = document.getElementById("task-list");
    list.innerHTML = "";

    data.tasks.forEach(task => {
        const li = document.createElement("li");
        const spanClass = task.done ? "done" : "";

         li.innerHTML = `
            <span class="${spanClass}">
                ${task.title}
            </span>
            <div>
                <button onclick="deleteTask(${task.id})">🗑️</button>
                <button onclick="toggleTask(${task.id}, ${task.done})">🔄</button>
            </div>
        `;

        list.appendChild(li);
    });
}
//Función para crear nuevas tareas
async function createTask() {
    const input = document.getElementById("task-input"); //Obtengo el input del HTML
    const title = input.value.trim(); //Obtengo el valor del input
    //Si no hay título, muestro un mensaje alertando
    if (!title) {
        alert("La tarea tiene que tener un título");
        return;
    }

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title }) //Envio el título en formato JSON al backend
    });

    input.value = ""; //Limpiamos el input
    loadTasks(); //Recargamos la lista para ver la nueva tarea
}
//Función para eliminar las tareas
async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}
//Función para cambiar el estado de las tareas(Hecho/No hecho)
async function toggleTask(id, currentDone) {
    await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ done: !currentDone })
    });

    loadTasks(); //Se recarga la lista para ver los cambios
}

loadTasks(); //Cargo las tareas para poder verlas de nuevo al recargar la página

//Cargamos las tareas cada vez que se usa una función para ver los cambios efectuados