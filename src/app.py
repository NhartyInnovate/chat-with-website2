from website_loader import load_website
from text_splitter import split_documents



url = "https://docs.langchain.com"

docs = load_website(url)

chunks = split_documents(docs)

print(f"Documents: {len(docs)}")
print(f"Chunks: {len(chunks)}")

print("\nFirst Chunk:")
print(chunks[0].page_content[:300])