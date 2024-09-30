# app/main.py

from fastapi import FastAPI, HTTPException
from app.schemas import Task, TaskCreate

# Initialize the app
app = FastAPI()

# In-memory "database" to store tasks
tasks = []
task_counter = 1  # Used to assign unique IDs

# CREATE: Add a new task
@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate):
    global task_counter
    new_task = Task(id=task_counter, title=task.title, description=task.description, completed=task.completed)
    tasks.append(new_task)
    task_counter += 1
    return new_task

# READ: Get all tasks
@app.get("/tasks/", response_model=list[Task])
def read_tasks(skip: int = 0, limit: int = 10):
    return tasks[skip: skip + limit]

# READ: Get a specific task
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# UPDATE: Update a task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskCreate):
    for task in tasks:
        if task.id == task_id:
            task.title = updated_task.title
            task.description = updated_task.description
            task.completed = updated_task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE: Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
