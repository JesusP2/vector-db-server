from typing import Literal, Union, List
from chromadb import Where
from pydantic import BaseModel


class QueryModel(BaseModel):
    q: str
    search_type: Union[Literal["short"], Literal["full"]] = "short"
    typee: Union[List[str], None] = None  # type is a reserved keyword
    subtype: Union[List[str], None] = None
    status: Union[List[str], None] = None
    authors: Union[List[str], None] = None
    genres: Union[List[str], None] = None
    themes: Union[List[str], None] = None
    demographics: Union[List[str], None] = None


def create_query(query: QueryModel) -> Where:
    metadata: dict = {"$or": []}
    if query.typee:
        metadata["$or"].append({"type": {"$in": query.typee}})
    if query.subtype:
        metadata["$or"].append({"subtype": {"$in": query.subtype}})
    if query.status:
        metadata["$or"].append({"status": {"$in": query.status}})

    if len(metadata["$or"]) == 0:
        del metadata["$or"]
    elif len(metadata["$or"]) == 1:
        metadata = metadata["$or"][0]
    return metadata
