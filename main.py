from src.graph import Workflow

app = Workflow().app
_id = "123"
chat_history = ""


def main():
    global chat_history
    while True:
        query = input("Enter your query: ")
        if query == "exit":
            break
        state = {"query": query, "user_id": _id, "chat_history": chat_history}
        response = app.invoke(state)
        print(response)
        chat_history += f"User: {query}\nAgent: {response['agent_output']['output']}\n"


if __name__ == "__main__":
    main()
