from crawler import get_links
from website_loader import load_website
from text_splitter import split_documents
from vector_store import add_chunks
from vector_store import get_indexed_pages

def index_website(url):

    urls = get_links(
        url,
        max_pages=20
    )

    indexed_pages = get_indexed_pages(url)

    new_urls = []

    for page in urls:

        if page not in indexed_pages:
            new_urls.append(page)


    urls.insert(0, url)

    print(
        f"Found {len(urls)} pages to index."
    )

    if not new_urls:

        print(
            "Everything is already indexed."
        )

        return

    docs = load_website(new_urls)

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