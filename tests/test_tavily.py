from dotenv import load_dotenv

load_dotenv()

from services.web_search import answer_from_web


def main() -> None:
    question = input("Question: ")

    result = answer_from_web(question)

    print("\nResults:\n")
    print(result)


if __name__ == "__main__":
    main()