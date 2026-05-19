from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow requests from Nuxt frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory task storage
tasks = []


# Request body model for creating a task
class TaskInput(BaseModel):
    title: str


# GET /tasks - return all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# POST /tasks - add a new task
@app.post("/tasks")
def add_task(task: TaskInput):
    new_task = {"title": task.title, "completed": False}
    tasks.append(new_task)
    return new_task


# DELETE /tasks/{index} - delete a task by index
@app.delete("/tasks/{index}")
def delete_task(index: int):
    if index < 0 or index >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    removed = tasks.pop(index)
    return removed


# PUT /tasks/{index} - mark a task as completed
@app.put("/tasks/{index}")
def complete_task(index: int):
    if index < 0 or index >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[index]["completed"] = True
    return tasks[index]
