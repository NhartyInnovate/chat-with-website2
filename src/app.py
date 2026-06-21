from website_loader import load_website
from text_splitter import split_documents
from llm import llm

from rag_pipeline import ask
from vector_store import (
   add_chunks,
   search
)



url = "https://docs.langchain.com/oss/python/langchain/overview"

docs = load_website(url)

chunks = split_documents(docs)

# print(f"Number of chunks: {len(chunks)}")

add_chunks(chunks)

question = "What is LangChain?"

# results = search(question)

# print(results["documents"][0][0])

answer = ask(question)

print(f"\nAnswer:")
print(answer)