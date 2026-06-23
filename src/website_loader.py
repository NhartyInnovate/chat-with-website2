from langchain_community.document_loaders import WebBaseLoader


def load_website(urls):
    loader = WebBaseLoader(
        web_path=urls
    )

    docs = loader.load()
    
    return docs