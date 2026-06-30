const API_URL = "http://127.0.0.1:5000/tasks";

async function loadTasks() {
    const response = await fetch(API_URL);
    const data = await response.json();

    const list = document.getElementById("task-list");
    list.innerHTML = "";

    data.tasks.forEach(task => {
        const li = document.createElement("li");

        li.innerHTML = `
            <span style="text-decoration: ${task.done ? 'line-through' : 'none'}">
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

async function createTask() {
    const input = document.getElementById("task-input");
    const title = input.value;

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ title })
    });

    input.value = "";
    loadTasks();
}

async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}

async function toggleTask(id, currentDone) {
    await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ done: !currentDone })
    });

    loadTasks();
}

loadTasks();