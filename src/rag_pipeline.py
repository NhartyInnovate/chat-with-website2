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
    the question at the end. 
    Context: {context}
    Question: {question}

    If you don't 
    know the answer, say:
    'I couldn't find that information on
    the website.'
    """


    response = llm.invoke(
        prompt
    )

    return response.content


