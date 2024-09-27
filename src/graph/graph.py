from langgraph.graph import END, StateGraph

from src.graph import Nodes, State


class Workflow:
    def __init__(self):
        self.supervisor_edges = {
            "customer-expert": "customer_expert",
            "transaction-expert": "transaction_expert",
            "complaints-expert": "complaints_expert",
        }
        nodes = Nodes()
        workflow = StateGraph(State)
        workflow.add_node("supervisor", nodes.supervisor)
        workflow.add_node("transaction_expert", nodes.transaction_expert)
        workflow.set_entry_point("supervisor")
        workflow.add_edge("supervisor", "transaction_expert")
        workflow.add_edge("transaction_expert", END)
        self.app = workflow.compile()
