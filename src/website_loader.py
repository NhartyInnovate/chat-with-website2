from langchain_community.document_loaders import WebBaseLoader


def load_website(url):
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs