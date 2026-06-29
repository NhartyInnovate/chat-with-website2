def classify_question(question):

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

    if question in small_talk:
        return "small_talk"

    return "knowledge"