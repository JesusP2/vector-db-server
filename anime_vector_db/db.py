from voyage import VoyageAIEmbeddingFunction
import chromadb
import voyageai
from env import env_vars

chroma_client = chromadb.PersistentClient()
voyageai.api_key = env_vars["VOYAGE_API_KEY"]
vo = voyageai.Client()
collection = chroma_client.get_collection(
    name=env_vars["COLLECTION_NAME"],
    embedding_function=VoyageAIEmbeddingFunction(
        api_key=env_vars["VOYAGE_API_KEY"],
        model_name=env_vars["MODEL_NAME"],
        batch_size=int(env_vars["BATCH_SIZE"]),
    ),
)
