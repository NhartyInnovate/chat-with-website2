from langchain_community.document_loaders import WebBaseLoader


def load_website(urls):
    loader = WebBaseLoader(
        web_path=urls
    )

    try:
        docs = loader.load()
        return docs

    except Exception as e:
        print(
            f"Loading Error: {e}"
        )
        return []
    
    return docs