from pydantic import BaseModel

class ToDoItem(BaseModel):
    task: str