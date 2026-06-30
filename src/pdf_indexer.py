from pdf_loader import load_pdf
from text_splitter import split_documents
from vector_store import add_chunks



def index_pdf(file_path):

    docs = load_pdf(file_path)

    if not docs:
        raise Exception(
            "Could not load PDF."
        )

    for doc in docs:
        print(
            f"{doc.metadata['source']}: "
            f"{len(doc.page_content)} characters"
        )

    chunks = split_documents(docs)

    add_chunks(chunks, file_path)

    print(
        f"Indexed {len(chunks)} chunks."
    )
