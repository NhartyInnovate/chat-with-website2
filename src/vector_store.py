from sentence_transformers import SentenceTransformer
import chromadb
from urllib.parse import urlparse


model = SentenceTransformer("all-MiniLM-L6-v2")


client = chromadb.PersistentClient(
    path="./chroma_db"
)

def add_chunks(chunks, url):
    collection = get_collection(url)
    for i, chunk in enumerate(chunks):
        embedding = model.encode(
            chunk.page_content
        ).tolist()
        
        collection.add(
            ids=[
                f"chunk_{i}"
            ],
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

        print(
            f"Stored chunk {i}"
        )
        print(
            f"Length: {len(chunk.page_content)}"
        )

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


def get_collection_name(url):
    parsed = urlparse(url)

    return (
        parsed.netloc
        .replace(".", "_")
        .replace("-", "_")
    )

def get_collection(url):
    collection_name = (
        get_collection_name(url)
    )

    return (
        client.get_or_create_collection(
            name=collection_name
        )
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