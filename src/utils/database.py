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
        for query, response, agent, timestamp in results[-5:]
    ]


def add_chat_history(user_id: str, query: str, response: str, agent: str):
    """
    Add a chat history entry
    """

    conn = sqlite3.connect("db/chat_history.db")
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO chat_histories (user_id, query, response, agent) VALUES ({user_id}, '{query}', '{response}', '{agent}')"
    )
    conn.commit()
    conn.close()


def get_user_data(user_id: str) -> dict[str, str]:
    """
    Retrieve user data for a given user
    """

    conn = sqlite3.connect("db/transactions.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT cc_num, first_name, last_name, gender, street, city, state, zip, dob FROM transactions WHERE user_id = {user_id} LIMIT 1"
    )
    results = cursor.fetchone()
    conn.close()
    return {
        "cc_num": results[0],
        "first_name": results[1],
        "last_name": results[2],
        "gender": results[3],
        "address": f"{results[4]}, {results[5]}, {results[6]} {results[7]}",
        "dob": results[8],
    }
