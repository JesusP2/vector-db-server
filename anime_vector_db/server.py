from typing import cast
from fastapi import FastAPI, WebSocket
import json
from db import collection
from functools import partial

from utils import QueryModel, create_query, filter_document


app = FastAPI()


@app.websocket("/q")
async def read_item(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        item = QueryModel(**data)
        metadata_filters = create_query(item)
        query = item.q
        collection.query(query_texts=query, )
        n_results = 10
        if item.search_type == "full":
            n_results = 25
        results = collection.query(query_texts=query, where=metadata_filters, n_results=n_results)
        if not results['documents']:
            await websocket.send_json(json.dumps([]))
            continue

        documents = cast(list, results['documents'][0] or [])
        if item.authors:
            filter_fn = partial(filter_document, entity="authors", filters=item.authors)
            documents = list(filter(filter_fn, documents))
        if item.genres:
            filter_fn = partial(filter_document, entity="genres", filters=item.genres)
            documents = list(filter(filter_fn, documents))
        if item.authors:
            filter_fn = partial(filter_document, entity="authors", filters=item.authors)
            documents = list(filter(filter_fn, documents))
        if item.themes:
            filter_fn = partial(filter_document, entity="themes", filters=item.themes)
            documents = list(filter(filter_fn, documents))
        if item.demographics:
            filter_fn = partial(filter_document, entity="demographics", filters=item.demographics)
            documents = list(filter(filter_fn, documents))
        await websocket.send_json(json.dumps(documents))
