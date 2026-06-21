from website_loader import load_website
from text_splitter import split_documents
from vector_store import clear_collection
from vector_store import add_chunks


def index_website(url):
    clear_collection()


    docs = load_website(url)

    chunks = split_documents(docs)

    add_chunks(chunks)

    print(
        f"Indexed {len(chunks)} chunks."
    )
