from fastapi import FastAPI, HTTPException
from uuid import uuid4
from app.schemas import Task, TaskCreate

# Initialize FastAPI app
app = FastAPI()

# In-memory storage (replace with MongoDB or SQLite for persistence)
global tasks  # Ensure persistence across function calls
tasks = []

# CREATE: Add a new task
@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    if not task.title or not task.description:  # Manual validation
        raise HTTPException(status_code=400, detail="Title and description are required")

    new_task = Task(
        id=str(uuid4()),  # Generate unique ID using UUID
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    tasks.append(new_task)

    # Log task creation instead of unnecessary failure check
    print(f"Task created successfully: {new_task.id}")

    if new_task not in tasks:
        raise HTTPException(status_code=500, detail="Task creation failed")

    return new_task

# READ: Get all tasks with pagination
@app.get("/tasks/", response_model=list[Task])
def read_tasks(skip: int = 0, limit: int = 10):
    return tasks[skip: skip + limit]

# READ: Get a specific task
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: str):
    try:
        task = next(task for task in tasks if task.id == task_id)
        return task
    except StopIteration:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

# UPDATE: Update a task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, updated_task: TaskCreate):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            tasks[idx] = Task(
                id=task_id,  # Preserve original ID
                title=updated_task.title,
                description=updated_task.description,
                completed=updated_task.completed
            )
            return tasks[idx]  # Return updated task
        
    raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

# DELETE: Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: str):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]