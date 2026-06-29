from llm import llm
from vector_store import search

def is_small_talk(question):

    question = question.lower().strip()

    small_talk = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "thanks",
        "thank you",
        "bye",
        "goodbye",
        "how are you"
    ]

    return question in small_talk

def ask(question, chat_history, source):

    if is_small_talk(question):

        responses = {
            "hi": "Hello! 👋",
            "hello": "Hi there! 👋",
            "hey": "Hey! 😊",
            "good morning": "Good morning! ☀️",
            "good afternoon": "Good afternoon! 😊",
            "good evening": "Good evening! 🌙",
            "thanks": "You're welcome! 😊",
            "thank you": "You're very welcome! 😊",
            "bye": "Goodbye! Have a great day! 👋",
            "goodbye": "Take care! 👋",
            "how are you": (
                "I'm doing great! "
                "How can I help you today?"
            )
        }

        return (
            responses.get(
            question.lower().strip(),
            "Hello! 👋"
            ),
            []
        )


    standalone_question = rewrite_question(question, chat_history)
    print(
    f"Standalone Question: "
    f"{standalone_question}"
    )
    results = search(
    standalone_question, source
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

    sources = results["metadatas"][0]

    return answer, sources


def rewrite_question(question, chat_history):
    if not chat_history:
        return question

    history = "\n".join(
        f"{role}: {message}"
        for role, message in chat_history
    )

    prompt = f"""
    You are an AI assistant.

    Your job is to rewrite the user's latest message
    into a complete standalone question.

    Use the conversation history to replace words like:

    - it
    - this
    - that
    - they
    - he
    - she
    - those

    with their actual meaning.

    If the latest question is already complete,
    return it unchanged.

    Conversation History:
    {history}

    Latest Question:
    {question}

    Standalone Question:
    """

    response = llm.invoke(prompt)

    return response.content