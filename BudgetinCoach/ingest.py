import os
import chromadb
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, CHROMA_PERSIST_DIR, GUIDES_DIR

# 1. Load embedding model
embedder = SentenceTransformer(EMBEDDING_MODEL)

# 2. Connect to ChromaDB (persistent local storage)
client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))
collection = client.get_or_create_collection(
    name="financial_guides",
    metadata={"hnsw:space": "cosine"}
)

# 3. Simple text splitter (no LangChain needed)
def chunk_text(text, chunk_size=500, overlap=50):
    """Splits text into overlapping word chunks."""
    words = text.split()
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

# 4. Ingest one file
def ingest_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text)
    if not chunks:
        print(f"No content to ingest in {filepath}")
        return
    ids = [f"{os.path.basename(filepath)}_{i}" for i in range(len(chunks))]
    embeddings = [embedder.encode(ch).tolist() for ch in chunks]
    metadatas = [{"source": os.path.basename(filepath)} for _ in chunks]
    collection.add(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)
    print(f"Ingested {len(chunks)} chunks from {filepath}")

# 5. Run ingestion on all .txt files in the guides folder
if __name__ == "__main__":
    if not GUIDES_DIR.exists():
        print(f"Guides folder not found at {GUIDES_DIR}. Creating it...")
        GUIDES_DIR.mkdir(parents=True, exist_ok=True)
        print("Please add .txt files to the 'guides' folder and run this script again.")
    else:
        ingested_count = 0
        for guide in os.listdir(GUIDES_DIR):
            if guide.endswith(".txt"):
                ingest_file(os.path.join(GUIDES_DIR, guide))
                ingested_count += 1
        if ingested_count == 0:
            print(f"No .txt files found in {GUIDES_DIR}. Add some financial guides and try again.")
        else:
            print("Ingestion complete.")