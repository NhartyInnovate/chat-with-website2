from sentence_transformers import SentenceTransformer
import chromadb


model = SentenceTransformer("all-MiniLM-L6-v2")


client = chromadb.Client()
collection = client.create_collection(
    name="website_chunks"
)

def add_chunks(chunks):
    for i, chunk in enumerate(chunks):
        embedding = model.encode(
            chunk.page_content
        ).tolist()
        
        collection.add(
            ids=[str(i)],
            documents=[chunk.page_content],
            embeddings=[embedding]
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
        n_results=2
    )

    print(f"Question: {query}")
    print(results)

    return results