from langchain.tools import tool


@tool
def retrieve_transaction_data(sql_query: str) -> str:
    """
    Retrieve data from a database using the given SQL query
    """
    # This function is a placeholder for a function that would actually fetch data from a database
    return "Rs. 1000"