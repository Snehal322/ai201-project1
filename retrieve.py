import chromadb

from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "csuf_rag"

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    COLLECTION_NAME
)

# ==========================
# Retrieval Function
# ==========================

def retrieve(query, k=4):

    query_embedding = model.encode(
        query
    )

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=k
    )

    return results


# ==========================
# Test Queries
# ==========================

queries = [

    "What engineering clubs are available for students interested in machine learning?",

    "What scholarships are available for international students?",

    "How can students get involved in campus events?"
]

for query in queries:

    print("\n" + "=" * 80)
    print("QUERY:")
    print(query)

    results = retrieve(query)

    docs = results["documents"][0]
    metadata = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(docs)):

        print("\n---------------------------")
        print(f"Rank #{i+1}")

        print(
            f"Source: {metadata[i]['source_file']}"
        )

        print(
            f"Distance: {distances[i]:.4f}"
        )

        print(
            docs[i][:500]
        )