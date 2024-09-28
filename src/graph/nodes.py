import json
from src.agents import Agents

ag = Agents()


class Nodes:
    def __init__(self):
        pass

    def supervisor(self, state) -> dict:
        query = state.get("query")
        chat_history = state.get("chat_history")
        result = ag.supervisor(query, chat_history)
        return {
            "agent_output": {"agent": "supervisor", "output": result},
        }

    def transaction_expert(self, state) -> dict:
        query = state.get("query")
        chat_history = state.get("chat_history")
        user_id = state.get("user_id")
        assert user_id is not None
        result = json.loads(ag.transaction_expert(query, chat_history, user_id))

        return {
            "agent_output": {
                "agent": "transaction_expert",
                "output": result["reply"],
                "trans_num": result.get("trans_num"),
            },
        }

    def customer_expert(self, state):
        query = state.get("query")
        chat_history = state.get("chat_history")
        result = json.loads(ag.customer_expert(query, chat_history))
        return {
            "agent_output": {"agent": "customer_expert", "output": result["reply"]},
        }

    def complaints_expert(self, state):
        query = state.get("query")
        chat_history = state.get("chat_history")
        user_id = state.get("user_id")
        assert user_id is not None
        result = ag.complaints_expert(query, chat_history, user_id)
        return {
            "agent_output": {"agent": "complaints_expert", "output": result},
        }
