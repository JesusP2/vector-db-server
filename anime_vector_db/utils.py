from typing import Literal, Union, List
from pydantic import BaseModel
from functools import partial


class QueryModel(BaseModel):
    q: str
    search_type: Union[Literal['short'], Literal['full']] = "short"
    typee: Union[List[str], None] = None  # type is a reserved keyword
    subtype: Union[List[str], None] = None
    status: Union[List[str], None] = None
    authors: Union[List[str], None] = None
    genres: Union[List[str], None] = None
    themes: Union[List[str], None] = None
    demographics: Union[List[str], None] = None


def create_query(query: QueryModel):
    metadata = {"$or": []}
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


def filter_document(document, filters: Union[List[str], None], entity: str):
    if filters:
        start = str.find(document, f";\n{entity}:")
        end = str.find(document, ";\n", start + 1)
        entity_list = list(map(lambda x: x.strip().lower(), document[start:end].split(":")[1].split(",")))
        filters = list(map(lambda x: x.strip().lower(), filters))
        if not set(entity_list).intersection(filters):
            return False
        return True
    return True

# filter_authors = partial(filter_document, entity="authors", filters=["author1", "author2"])
# filter(filter_authors, document)
