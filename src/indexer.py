from crawler import get_links
from website_loader import load_website
from text_splitter import split_documents
from vector_store import add_chunks


def index_website(url):

    urls = get_links(
        url,
        max_pages=20
    )

    urls.insert(0, url)

    print(
        f"Found {len(urls)} pages to index."
    )

    print("URLs to load:")

    for page_url in urls:
        print(page_url)

    docs = load_website(urls)

    if not docs:
        raise Exception(
            "Could not load website."
        )

    for doc in docs:
        print(
            f"{doc.metadata['source']}: "
            f"{len(doc.page_content)} characters"
        )

    chunks = split_documents(docs)

    add_chunks(chunks, url)

    print(
        f"Indexed {len(chunks)} chunks."
    )

    print("Pages Found:")

    for page_url in urls:
        print(page_url)