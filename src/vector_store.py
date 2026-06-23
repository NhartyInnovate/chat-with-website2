from sentence_transformers import SentenceTransformer
import chromadb


model = SentenceTransformer("all-MiniLM-L6-v2")


client = chromadb.PersistentClient(
    path="./chroma_db"
)
collection = (
    client.get_or_create_collection(
        name="website_chunks"
    )
)

def add_chunks(chunks):
    for i, chunk in enumerate(chunks):
        embedding = model.encode(
            chunk.page_content
        ).tolist()
        
        collection.add(
            ids=[str(i)],
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

def search(query):
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

def clear_collection():
    global collection

    try:
        client.delete_collection(
            "website_chunks"
        )
    except:
        pass

    collection = (
        client.get_or_create_collection(
            "website_chunks"
        )
    )