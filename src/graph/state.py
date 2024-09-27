from typing import TypedDict


class State(TypedDict):
    query: str
    user_id: str
    chat_history: str
    agent_output: str
