import json
import chromadb

from sentence_transformers import SentenceTransformer

# ==========================
# Configuration
# ==========================

CHUNKS_FILE = "chunks.json"
COLLECTION_NAME = "csuf_rag"

# ==========================
# Load Chunks
# ==========================

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

# ==========================
# Embedding Model
# ==========================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded")

# ==========================
# ChromaDB
# ==========================

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={
        "hnsw:space": "cosine"
    }
)

# ==========================
# Create Embeddings
# ==========================

documents = []
ids = []
metadatas = []

for chunk in chunks:

    documents.append(
        chunk["chunk_text"]
    )

    ids.append(
        str(chunk["chunk_id"])
    )

    metadatas.append({
        "source_file":
            chunk["source_file"],
        "chunk_id":
            chunk["chunk_id"]
    })

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

# ==========================
# Store in Chroma
# ==========================

collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print(
    f"Stored {len(documents)} chunks in ChromaDB"
)