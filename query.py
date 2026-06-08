import os
from dotenv import load_dotenv
from groq import Groq

import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# Load API Key
# -----------------------------

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# Load Embedding Model
# -----------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------
# Connect ChromaDB
# -----------------------------

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_collection(
    "csuf_rag"
)

# -----------------------------
# Retrieval
# -----------------------------

def retrieve(query, k=4):

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    retrieved_chunks = results["documents"][0]
    metadata = results["metadatas"][0]

    return retrieved_chunks, metadata


# -----------------------------
# Ask Function
# -----------------------------

def ask(question):

    chunks, metadata = retrieve(question)

    context = "\n\n".join(chunks)

    sources = list(
        set(
            item["source_file"]
            for item in metadata
        )
    )

    prompt = f"""
You are a CSUF Engineering Student Assistant.

Answer ONLY using the provided context.

If the answer is not contained in the context,
respond exactly:

I don't have enough information on that.

CONTEXT:
{context}

QUESTION:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }