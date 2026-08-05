"""
Command-line interface for the
Intelligent Agentic Research Assistant.
"""

from dotenv import load_dotenv

# Load environment variables BEFORE importing services.
load_dotenv()

from config.settings import MAX_CONVERSATION_MESSAGES
from services.conversation import ConversationService
from services.conversation_memory import ConversationMemory
from services.pipeline import initialize_pipeline


def main() -> None:
    """
    Start the research assistant.
    """

    vector_store = initialize_pipeline()

    memory = ConversationMemory(
        max_messages=MAX_CONVERSATION_MESSAGES,
    )

    conversation = ConversationService(
        vector_store=vector_store,
        memory=memory,
    )

    print("🤖 Intelligent Agentic Research Assistant")
    print("Type 'exit' to quit.")
    print("Type 'clear' to clear conversation memory.\n")

    while True:
        question = input("You: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            print("\n👋 Goodbye!")
            break

        if question.lower() == "clear":
            conversation.clear()

            print("\n🧹 Conversation memory cleared.\n")
            continue

        response = conversation.ask(
            question,
        )

        if response is None:
            print(
                "\nI need more context to understand "
                "your question. Please clarify what "
                "you are referring to.\n"
            )
            continue

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
