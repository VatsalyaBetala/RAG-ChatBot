from chat import ask_question

def main():
    print("RAG ChatBot (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        try:
            answer = ask_question(user_input)
            print("Bot:", answer)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
