from fastapi import FastAPI, HTTPException
from uuid import uuid4
from app.schemas import Task, TaskCreate

app = FastAPI()

# In-memory storage
tasks: list[Task] = []

# CREATE: Add a new task
@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    if not task.title or not task.description:
        raise HTTPException(status_code=400, detail="Title and description are required")

    new_task = Task(
        id=str(uuid4()),
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    tasks.append(new_task)
    return new_task

# READ: Get all tasks (with pagination)
@app.get("/tasks/", response_model=list[Task])
def read_tasks(skip: int = 0, limit: int = 10):
    return tasks[skip: skip + limit]

# READ: Get a specific task
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# UPDATE: Update a task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated_task: TaskCreate):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            tasks[idx] = Task(
                id=task_id,
                title=updated_task.title,
                description=updated_task.description,
                completed=updated_task.completed
            )
            return tasks[idx]
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE: Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
