from typing import cast
from fastapi import FastAPI, WebSocket
import json
from db import collection

from utils import QueryModel, create_query


app = FastAPI()


@app.websocket("/q")
async def read_item(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        body = QueryModel(**data)
        if body.q == "":
            await websocket.send_json([])
            continue
        metadata_filters = create_query(body)
        query = body.q
        n_results = 10
        if body.search_type == "full":
            n_results = 25
        results = collection.query(
            query_texts=query, where=metadata_filters, n_results=n_results
        )
        if not results["documents"] or not results["metadatas"]:
            await websocket.send_json([])
            continue

        filters = {
            "authors": body.authors,
            "genres": body.genres,
            "themes": body.themes,
            "demographics": body.demographics,
        }
        documents = cast(list, results["documents"][0] or [])
        metadata = results["metadatas"][0]
        for entity, filters in filters.items():
            if filters and len(filters) > 0:
                filtered_metadata = []
                for i in range(len(metadata)):
                    document = documents[i]
                    start = str.find(document, f";\n{entity}:")
                    end = str.find(document, ";\n", start + 1)
                    entity_list = list(
                        map(
                            lambda x: x.strip().lower(),
                            document[start:end].split(":")[1].split(","),
                        )
                    )
                    filters = list(map(lambda x: x.strip().lower(), filters))
                    if set(entity_list).intersection(filters):
                        filtered_metadata.append(metadata[i])
                    else:
                        pass
                metadata = filtered_metadata
        await websocket.send_json(metadata)
