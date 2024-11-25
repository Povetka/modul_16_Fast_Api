from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")

messages_db = []


class Message(BaseModel):
    id: int = None
    text: str


@app.get("/")
def get_all_messages(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('message.html', {'request': request, 'messages': messages_db})


@app.get(path="/message/{message_id}")
def get_message(message_id: int) -> Message:
    try:
        return messages_db[message_id]
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/message")
def create_message(message: Message) -> str:
    message.id = len(messages_db)
    messages_db.append(message)
    return f"Message created!"


@app.put("/message/{message_id}")
def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return f"Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/message/{message_id}")
def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/")
def kill_message_all() -> str:
    messages_db.clear()
    return "All_messages_deleted!"

# python -m uvicorn main:app
