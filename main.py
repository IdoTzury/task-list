from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1

class Task(BaseModel):
    title: str
    owner: str
    priority: int = Field(default=2, ge=1, le=3)
@app.get("/tasks")
def get_tasks(priority: int | None = Query(default = None, ge=1, le=3)):
    if priority is not None:
        return [task for task in tasks if task["priority"] == priority] # List Comprehension
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks")
def add_task(task: Task):
    global counter
    new_task = {
        "id": counter,
        "title": task.title,
        "owner": task.owner,
        "priority": task.priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
