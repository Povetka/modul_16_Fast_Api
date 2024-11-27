from fastapi import FastAPI, status, Body, HTTPException, Request, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates_dz")

users = {}


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
def get_user(request: Request, user_id: int):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}")
async def create_user(username: str, age) -> str:
    user_id = str(len(users) + 1)
    users[user_id] = User(id=int(user_id), username=username, age=int(age))
    return f"User {user_id} is registered"


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: int, username: str, age: int) -> str:
    users[user_id] = f"Имя: {username}, возраст: {age}"
    return f"The user {user_id} is updated"


@app.delete("/user/{user_id}")
async def delete_user(user_id: str) -> str:
    users.pop(user_id)
    return f'User {user_id} has been deleted'

# python -m uvicorn module_16_5:app
