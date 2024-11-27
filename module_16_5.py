from fastapi import FastAPI, HTTPException, Request, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Annotated

app = FastAPI()

templates = Jinja2Templates(directory="templates_dz")

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/")
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/user/{user_id}")
def get_user(request: Request, user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) \
        -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user/{username}/{age}")
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20,
                                                    description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(le=120, ge=18, description='Enter age', example='24')]) -> User:
    user_id = str(len(users) + 1)
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                      username: Annotated[str, Path(min_length=5, max_length=20,
                                                    description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(le=120, ge=18, description='Enter age', example='24')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User was not found')


@app.delete("/user/{user_id}")
async def delete_user(user_id: str) -> str:
    users.remove(user_id)
    return f'User {user_id} has been deleted'

# python -m uvicorn module_16_5:app
