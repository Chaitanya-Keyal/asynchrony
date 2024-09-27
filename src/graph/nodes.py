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
        result = ag.transaction_expert(query, chat_history, user_id)
        return {
            "agent_output": {"agent": "transaction_expert_agent", "output": result},
        }
