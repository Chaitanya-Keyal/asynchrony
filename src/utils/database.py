import sqlite3


def init_db():
    conn = sqlite3.connect("db/chat_history.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chat_histories (
            user_id INTEGER,
            query TEXT,
            response TEXT,
            agent TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def get_chat_history(user_id: str) -> list[dict[str, str]]:
    """
    Retrieve chat history for a given user
    """

    conn = sqlite3.connect("db/chat_history.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT query, response, agent, timestamp FROM chat_histories WHERE user_id = {user_id} ORDER BY timestamp ASC"
    )
    results = cursor.fetchall()
    conn.close()

    return [
        {"query": query, "response": response, "agent": agent, "timestamp": timestamp}
        for query, response, agent, timestamp in results
    ]


def add_chat_history(user_id: str, query: str, response: str, agent: str):
    """
    Add a chat history entry
    """

    conn = sqlite3.connect("db/chat_history.db")
    cursor = conn.cursor()
    print(
        f"INSERT INTO chat_histories (user_id, query, response, agent) VALUES ({user_id}, '{query}', '{response}', '{agent}')"
    )
    cursor.execute(
        f"INSERT INTO chat_histories (user_id, query, response, agent) VALUES ({user_id}, '{query}', '{response}', '{agent}')"
    )
    conn.commit()
    conn.close()
