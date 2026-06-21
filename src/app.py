from indexer import index_website
from rag_pipeline import ask

url = input(
    "Enter website URL: "
)

index_website(url)

while True:
    question = input(
        "\nAsk a question: "
    )

    if question.lower() == "quit":
        break

    answer = ask(question)

    print("\nAnswer:")
    
    print(answer)

