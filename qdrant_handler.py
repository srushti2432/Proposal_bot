# qdrant_handler.py

from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Read config
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# Init
client = QdrantClient(url=QDRANT_URL)
embedder = SentenceTransformer(EMBEDDING_MODEL)

# Same functions as before
def create_collection():
    if not client.collection_exists(QDRANT_COLLECTION):
        client.recreate_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=models.VectorParams(
                size=embedder.get_sentence_embedding_dimension(),
                distance=models.Distance.COSINE
            )
        )

def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def upsert_document(text):
    create_collection()
    chunks = chunk_text(text)
    vectors = embedder.encode(chunks).tolist()
    points = [
        models.PointStruct(id=i, vector=vec, payload={"text": chunk})
        for i, (chunk, vec) in enumerate(zip(chunks, vectors))
    ]
    client.upsert(collection_name=QDRANT_COLLECTION, points=points)
    print(f"✅ Indexed {len(points)} chunks in Qdrant.")

def semantic_search(query, top_k=3):
    query_vec = embedder.encode(query).tolist()
    results = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vec,
        limit=top_k
    )
    return [hit.payload['text'] for hit in results]
