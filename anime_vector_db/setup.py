import os
import chromadb
from tenacity import sleep
import voyageai
import csv
import json
from voyage import VoyageAIEmbeddingFunction
from typing import List, Dict, Union, Literal
from env import env_vars

START = 0
END = 240
CREATE = True
BATCH_SIZE = int(env_vars['BATCH_SIZE'])
FILES = [
    {'anime': './anime_anime_rows.csv'},
    # {'manga': './anime_manga_rows.csv'},
    # { 'character': './anime_character_rows.csv'}
]
dir_name = os.path.dirname(os.path.realpath(__file__))
chroma_client = chromadb.PersistentClient(os.path.join(dir_name, "chroma"))
vo = voyageai.Client()
if CREATE:
    chroma_client.delete_collection(name = env_vars['COLLECTION_NAME'])
    collection = chroma_client.create_collection(
        name = env_vars['COLLECTION_NAME'],
        metadata = { "source": "myanimelist" },
        embedding_function= VoyageAIEmbeddingFunction(
            api_key = env_vars['VOYAGE_API_KEY'],
            model_name = env_vars['MODEL_NAME'],
            batch_size = BATCH_SIZE
        ),
    )
else:
    collection = chroma_client.get_collection(
        name = env_vars['COLLECTION_NAME'],
        embedding_function= VoyageAIEmbeddingFunction(
            api_key = env_vars['VOYAGE_API_KEY'],
            model_name = env_vars['MODEL_NAME'],
            batch_size = BATCH_SIZE
        ),
    )

records = []
with open('./anime_anime_rows.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        records.append(row)

ItemKey = Union[
    Literal['title'],
    Literal['type'],
    Literal['status'],
    Literal['score'],
    Literal['synopsis'],
    Literal['background'],
    Literal['authors'],
    Literal['genres'],
    Literal['themes'],
    Literal['demographics'],
    Literal['mal_id'],
    Literal['id'],
]
GenericItem = List[Dict[Union[Literal['mal_id'], Literal['type'], Literal['name'], Literal['url']], str]]
def parseStringifiedArray(item: Dict[ItemKey, Union[str, GenericItem]], key: ItemKey):
    prop = item[key];
    if isinstance(prop, str):
        prop = json.loads(prop)
    else:
        prop = []
    
    if isinstance(prop, list):
        return ",".join(list(map(lambda x: x['name'], prop)))
    return ""

def createVector(record: Dict[ItemKey, Union[str, GenericItem]], record_type: str):
    document = ''
    if 'synopsis' in record and isinstance(record['synopsis'], str):
        document += f"synopsis: {record['synopsis']}\n"
    if 'background' in record and isinstance(record['background'], str):
        document += f"background: {record['background']}\n"
    if 'authors' in record:
        authors = parseStringifiedArray(record, 'authors')
        document += f"authors: {authors}\n"
    if 'genres' in record:
        genres = parseStringifiedArray(record, 'genres')
        document += f"genres: {genres}\n"
    if 'themes' in record:
        themes = parseStringifiedArray(record, 'themes')
        document += f"themes: {themes}\n"
    if 'demographics' in record:
        demographics = parseStringifiedArray(record, 'demographics')
        document += f"demographics: {demographics}\n"

    metadata = {
        'type': record_type
    }
    if 'title' in record and isinstance(record['title'], str):
        metadata['title'] = record['title']
    if 'type' in record and isinstance(record['type'], str):
        metadata['subtype'] = record['type']
    if 'status' in record and isinstance(record['status'], str):
        metadata['status'] = record['status']
    if 'score' in record and isinstance(record['score'], (str, int)):
        metadata['score'] = record['score']
    if 'mal_id' in record and isinstance(record['mal_id'], (str, int)):
        metadata['mal_id'] = record['mal_id']

    return [record['id'], metadata, document]

ids = []
metadatas = []
documents = []
for i, record in enumerate(records):
    [id, metadata, document] = createVector(record, "anime")
    ids.append(id)
    metadatas.append(metadata)
    documents.append(document)
if END == 0:
    END = len(ids)

for i in range(START, END, BATCH_SIZE):
    print(f"Processing {i} to {i + BATCH_SIZE} of {END}")
    collection.add(
        ids = ids[i : i + BATCH_SIZE],
        metadatas = metadatas[i : i + BATCH_SIZE],
        documents = documents[i : i + BATCH_SIZE]
    )
    sleep(1)
