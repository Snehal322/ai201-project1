# import requests
# from bs4 import BeautifulSoup
from pathlib import Path
import html
import json
import re
import time

import random


import gradio as gr
from query import ask

# ==========================
# Configuration
  
RAW_DIR = "raw_documents"
OUTPUT_FILE = "chunks.json"

CHUNK_SIZE = 200
OVERLAP = 40

 
 
# ==========================
# Load Documents
 

def load_documents():

    docs = []

    for file in Path(RAW_DIR).glob("*.txt"):

        try:
            with open(
                file,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                text = f.read().strip()

            docs.append({
                "source_file": file.name,
                "text": text
            })

        except Exception as e:
            print(f"Error loading {file}")
            print(e)

    return docs

# ==========================
# Chunking
 
def chunk_text(
    text,
    chunk_size=255,
    overlap=50
    ):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        if end >= len(words):
            break

        start += (
            chunk_size - overlap
        )

    return chunks

# ====================================
# CREATE CHUNKS 

def create_chunk_records(documents):

    records = []

    chunk_id = 1

    for doc in documents:

        doc_chunks = chunk_text(
            doc["text"],
            CHUNK_SIZE,
            OVERLAP
        )

        for chunk in doc_chunks:

            records.append({
                "chunk_id": chunk_id,
                "source_file": doc["source_file"],
                "chunk_text": chunk
            })

            chunk_id += 1

    return records

# ====================================
# MAIN 

def main():

    print("\nLoading Documents...\n")

    documents = load_documents()

    if not documents:
        print("No documents found in raw_documents/")
        return
    
    print("\n Documents Loaded: \n")

    for doc in documents:
        print(f"- {doc['source_file']}")

    print(
        f"Documents Loaded: {len(documents)} \n \n"
    )

    print("\n Document Preview: \n")

    print(
        documents[0]["text"][:1000]
    )

    print("\nCreating chunks... \n \n")

    chunks = create_chunk_records(
        documents
    )

    print(
        f"Total Chunks: {len(chunks)} \n \n"
    )

    chunk_lengths = [
    len(chunk["chunk_text"].split())
    for chunk in chunks
    ]

    avg_chunk_size = (
        sum(chunk_lengths) / len(chunk_lengths)
    )

    print(f"Average Chunk Size: {avg_chunk_size:.1f} words \n")
    print(f"Min Chunk Size: {min(chunk_lengths)} words \n")
    print(f"Max Chunk Size: {max(chunk_lengths)} words \n")

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f" Saved chunks to {OUTPUT_FILE} \n \n"
    )

    print("\n * Sample Chunks: \n  ")
 

    print("\n===== RANDOM SAMPLE CHUNKS =====\n")

    sample_chunks = random.sample(
            chunks,
            min(5, len(chunks))
        )

    for chunk in sample_chunks:

        print("=" * 80)

        print(
            f"Chunk #{chunk['chunk_id']} \n"
        )

        print(
            f"Source: {chunk['source_file']} \n"
        )

        print("-" * 80)

        print(
            chunk["chunk_text"][:800]
        )

        print()

    # checking empty chunks

    empty_chunks = [
    c for c in chunks
    if len(c["chunk_text"].strip()) == 0
    ]

    print(f" * Empty Chunks: {len(empty_chunks)} \n \n")

    # ==========================
    #  Verifying src metadata

    from collections import Counter

    sources = Counter(
        chunk["source_file"]
        for chunk in chunks
    )

    print("\n * Chunks Per Document: \n \n")

    for source, count in sources.items():
        print(f"{source}: {count} \n \n")



# -----------------------------

def handle_query(question):

    result = ask(question)

    sources = "\n".join(
        f"• {s}"
        for s in result["sources"]
    )

    return (
        result["answer"],
        sources
    )

# -----------------------------

with gr.Blocks() as demo:

    gr.Markdown(
        "# CSUF Engineering Student Guide"
    )

    gr.Markdown(
        "Ask questions about clubs, scholarships, housing, events, resources, and graduate programs."
    )

    question = gr.Textbox(
        label="Ask a Question"
    )

    ask_button = gr.Button(
        "Ask"
    )

    answer = gr.Textbox(
        label="Answer",
        lines=10
    )

    sources = gr.Textbox(
        label="Sources",
        lines=5
    )

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[
            answer,
            sources
        ]
    )

    question.submit(
        handle_query,
        inputs=question,
        outputs=[
            answer,
            sources
        ]
    )

demo.launch()

if __name__== "__main__":
    main()