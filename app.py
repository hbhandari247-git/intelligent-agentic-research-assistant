"""
Command-line interface for the
Intelligent Agentic Research Assistant.
"""

from dotenv import load_dotenv

# Load environment variables BEFORE importing services.

load_dotenv()

from config.settings import MAX_CONVERSATION_MESSAGES
from models.collection import Collection
from services.conversation import ConversationService
from services.conversation_memory import ConversationMemory
from services.index_manager import IndexManager
from services.pipeline import initialize_pipeline


def _select_collection(
    index_manager: IndexManager,
) -> Collection:
    """
    Prompt the user to select a document collection.
    """

    collections = index_manager.list_collections()

    if not collections:
        raise RuntimeError("No document collections found.")

    print("\n📚 Available collections:\n")

    for selection_index, collection in enumerate(
        collections,
        start=1,
    ):
        print(
            f"{selection_index}. "
            f"{collection.name} "
            f"({collection.document_count} documents)"
        )

    collection_lookup = {
        collection.name.lower(): collection for collection in collections
    }

    while True:

        selection = input("\nSelect a collection: ").strip()

        if selection.isdigit():

            selection_index = int(selection)

            if 1 <= selection_index <= len(collections):
                return collections[selection_index - 1]

        else:

            collection = collection_lookup.get(selection.lower())

            if collection is not None:
                return collection

        print("Invalid collection. Please try again.")


def main() -> None:
    """
    Start the research assistant.
    """

    index_manager = initialize_pipeline()

    try:
        collection = _select_collection(
            index_manager,
        )

    except RuntimeError as error:
        print(f"❌ {error}")
        return

    vector_store = index_manager.get_vector_store(
        collection.name,
    )

    memory = ConversationMemory(
        max_messages=MAX_CONVERSATION_MESSAGES,
    )

    conversation = ConversationService(
        vector_store=vector_store,
        memory=memory,
    )

    print("\n🤖 Intelligent Agentic Research Assistant")
    print(f"📚 Collection: {collection.name}")
    print("Type 'exit' to quit.")
    print("Type 'clear' to clear conversation memory.\n")

    while True:

        question = input("You: ").strip()

        if not question:
            continue

        match question.lower():

            case "exit":
                print("\n👋 Goodbye!")
                break

            case "clear":
                conversation.clear()
                print("\n🧹 Conversation memory cleared.\n")
                continue

        response = conversation.ask(question)

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
