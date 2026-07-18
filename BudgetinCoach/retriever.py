from sentence_transformers import SentenceTransformer
import chromadb
from config import EMBEDDING_MODEL, CHROMA_PERSIST_DIR

embedder = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))
collection = client.get_collection("financial_guides")

def retrieve(query, top_k=3):
    query_emb = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_emb], n_results=top_k)
    docs = results["documents"][0] if results["documents"] else []
    sources = [m["source"] for m in results["metadatas"][0]] if results["metadatas"] else []
    return docs, sources