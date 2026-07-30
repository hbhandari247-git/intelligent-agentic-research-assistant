"""
Command-line interface for the
Intelligent Agentic Research Assistant.
"""

from dotenv import load_dotenv

# Load environment variables BEFORE importing services.
load_dotenv()

from services.pipeline import initialize_pipeline
from services.router import route_question


def main() -> None:
    """
    Start the research assistant.
    """

    # Initialize the application.
    vector_store = initialize_pipeline()

    print("🤖 Intelligent Agentic Research Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("\n👋 Goodbye!")
            break

        if not question:
            continue

        response = route_question(
            vector_store,
            question,
        )

        print()

        print(response.answer)

        print(f"\nSource: {response.source.value}")

        print(f"Confidence: {response.confidence.value}")

        if response.citations:
            print("\nReferences:")

            for citation in response.citations:
                print(f"- {citation.title}")

                print(f"  {citation.location}")

                if citation.url:
                    print(f"  {citation.url}")

        print()


if __name__ == "__main__":
    main()
