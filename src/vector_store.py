from sentence_transformers import SentenceTransformer
import chromadb
from urllib.parse import urlparse
import os
import re
import streamlit as st


@st.cache_resource
def load_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


model = load_model()

@st.cache_resource
def get_client():
    
    return chromadb.PersistentClient(
        path="./data/chroma_db"
    )


client = get_client()

def add_chunks(chunks, url):

    print("1. Entered add_chunks()")

    collection = get_collection(url)

    print("2. Collection obtained")

    for i, chunk in enumerate(chunks):

        print(f"3. Processing chunk {i}")

        embedding = model.encode(
            chunk.page_content
        ).tolist()

        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk.page_content],
            embeddings=[embedding],
            metadatas=[
                {
                    "chunk": i,
                    "source": chunk.metadata.get(
                        "source",
                        "Unknown"
                    )
                }
            ]
        )

        print(f"Stored chunk {i}")

def search(query, url):
    collection = get_collection(url)
    query_embedding = model.encode(
        query
    ).tolist()


    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    print(f"Question: {query}")
    print(results)

    return results


def get_collection_name(source):

    if source.startswith("http"):

        parsed = urlparse(source)

        return (
            parsed.netloc
            .replace(".", "_")
            .replace("-", "_")
        )

    filename = os.path.basename(source)

    filename = filename.replace(".pdf", "")

    filename = re.sub(
        r"[^a-zA-Z0-9._-]",
        "_",
        filename
    )

    filename = filename.strip("._-")

    return filename

def get_collection(url):

    collection_name = get_collection_name(url)

    print(f"URL/Source: {url}")
    print(f"Collection Name: {collection_name}")

    return client.get_or_create_collection(
        name=collection_name
    )

def get_collections():
    collections = (
        client.list_collections()
    )
    return [
        collection.name
        for collection in collections
    ]

def display_name(
    collection_name
):
    return (
        collection_name
        .replace("_", ".")
    )


def get_indexed_pages(url):
    collection = get_collection(url)

    data = collection.get()

    indexed_pages = {
        metadata["source"]
        for metadata in data["metadatas"]
    }

    return indexed_pages