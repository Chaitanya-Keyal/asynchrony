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
        result = ag.transaction_expert(query, chat_history)
        return {
            "agent_output": {"agent": "transaction_expert_agent", "output": result},
        }