from typing import List
from pydantic import BaseModel

from fastapi import FastAPI, status, HTTPException

app = FastAPI()


class todo_item(BaseModel):
    id: int
    text: str


fake_db: List[todo_item] = [
    todo_item(id=1, text="Buy milk"),
    todo_item(id=2, text="Walk the dog"),
    todo_item(id=3, text="Do laundry"),
    todo_item(id=4, text="Call John"),
    todo_item(id=5, text="Finish project report"),
]


@app.get("/list", status_code=status.HTTP_200_OK)
def get_todo_list(page: int = 1, per_page: int = 10, filter_text: str = "") -> dict:
    filtered_db = [item for item in fake_db if filter_text.lower() in item.text.lower()]
    sorted_db = sorted(filtered_db, key=lambda x: getattr(x, "id"))

    total_pages = -(-len(sorted_db) // per_page)
    current_page = page
    current_items = sorted_db[(page - 1) * per_page:page * per_page]

    return {
        "items": current_items,
        "total_pages": total_pages,
        "current_page": current_page,
        "per_page": per_page,
    }


@app.get("/item/{id}", status_code=status.HTTP_200_OK)
def get_todo_by_id(id: int) -> todo_item:
    for item in fake_db:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail=f"Todo item with id {id} not found")


@app.post('/item', status_code=status.HTTP_200_OK)
def create_todo(data: str) -> todo_item:
    new_todo = todo_item(id=len(fake_db) + 1, text=data)
    fake_db.append(new_todo)
    return new_todo


@app.put("/item/{id}")
def update_todo_by_id(id: int, data: str) -> todo_item:
    for item in fake_db:
        if item.id == id:
            item.text = data
            return item
    raise HTTPException(status_code=404, detail=f"Todo item with id {id} not found")


@app.delete("/item/{id}")
def delete_todo_by_id(id: int) -> str:
    for item in fake_db:
        if item.id == id:
            fake_db.remove(item)
            return f"Todo item with id {id} deleted successfully"
    raise HTTPException(status_code=404, detail=f"Todo item with id {id} not found")
