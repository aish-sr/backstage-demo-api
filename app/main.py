from fastapi import FastAPI, HTTPException
from app.models import ToDo
from app.schemas import ToDoItem
import json
from typing import List

app = FastAPI(title="Simple ToDo API", version="1.0.0")

DATA_FILE = "app/todo_data.json"

def read_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the ToDo API"}

@app.get("/todos", response_model=List[ToDoItem])
def get_todos():
    return read_data()

@app.post("/todos", response_model=ToDoItem)
def create_todo(item: ToDoItem):
    todos = read_data()
    todos.append(item.model_dump())
    write_data(todos)
    return item

@app.delete("/todos/{task}", status_code=204)
def delete_todo(task: str):
    todos = read_data()
    new_todos = [todo for todo in todos if todo["task"] != task]
    if len(todos) == len(new_todos):
        raise HTTPException(status_code=404, detail="Task not found")
    write_data(new_todos)
