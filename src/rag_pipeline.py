from llm import llm
from vector_store import search



def ask(question):
    results = search(question)


    context = "\n\n".join(
        results["documents"][0]
    )

    prompt = f"""
    You are a helpful assistant. Use the 
    following pieces of context to answer 
    the question at the end. If you don't 
    know the answer, say you don't know.
    Context: {context}
    Question: {question}
    """


    response = llm.invoke(
        prompt
    )

    return response.content


