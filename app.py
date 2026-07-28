"""
Command-line interface for the
Intelligent Agentic Research Assistant.
"""

from dotenv import load_dotenv

# Load environment variables BEFORE importing services
load_dotenv()

from services.pipeline import initialize_pipeline
from services.rag import answer_from_pdf


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

        answer = answer_from_pdf(
            vector_store,
            question,
        )

        if answer is None:
            print("\n🌐 This question is outside the PDF.")
            print("🔜 Tavily Web Search will be integrated next.\n")
        else:
            print(f"\n🤖 {answer}\n")


if __name__ == "__main__":
    main()