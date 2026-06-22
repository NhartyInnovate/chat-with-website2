from llm import llm
from vector_store import search



def ask(question, chat_history):
    standalone_question = rewrite_question(question, chat_history)
    print(
    f"Standalone Question: "
    f"{standalone_question}"
    )
    results = search(
    standalone_question
)

    if not results["documents"][0]:
        return (
            "I couldn't find that "
            "information on the website."
        )

    context = "\n\n".join(
        results["documents"][0]
    )

    prompt = f"""
    You are a helpful assistant.

        Use ONLY the information in the context below.

        Provide detailed answers.

        If possible:
        - explain concepts
        - include examples
        - summarize important points

        Context:
        {context}

        Question:
        {standalone_question}

        Answer:
    """


    response = llm.invoke(
        prompt
    )

    answer = response.content

    return answer


def rewrite_question(question, chat_history):
    if not chat_history:
        return question

    history = "\n".join(
        f"{role}: {message}"
        for role, message in chat_history
    )

    prompt = f"""
    Given the conversation history and the
    latest user question, rewrite the latest
    question into a standalone question.

    History:
    {history}

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return response.content