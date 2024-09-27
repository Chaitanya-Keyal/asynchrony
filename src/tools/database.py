from langchain.tools import tool
import sqlite3
from typing import Any


@tool
def retrieve_transaction_data(sql_query: str) -> list[Any]:
    """
    Retrieve data from a database using the given SQL query
    """

    print("Tool is being used", sql_query)
    conn = sqlite3.connect("src/db/transactions.db")
    cursor = conn.cursor()
    # FIX: only fetch do not insert or update
    cursor.execute(sql_query)
    result = cursor.fetchall()
    conn.close()
    print("Tool result", result)

    return result
