from typing import Union, List
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import json

class Query(BaseModel):
    q: str
    typee: Union[List[str], None] = None # type is a reserved keyword
    subtype: Union[List[str], None] = None
    status: Union[List[str], None] = None
    authors: Union[List[str], None] = None
    genres: Union[List[str], None] = None
    themes: Union[List[str], None] = None
    demographics: Union[List[str], None] = None

app = FastAPI()


@app.websocket("/q")
async def read_item(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = json.loads(await websocket.receive_text())
        item = Query(**data)
        await websocket.send_text(f"Message text was: {item.model_dump_json()}")
