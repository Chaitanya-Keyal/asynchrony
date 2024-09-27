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
        workflow.set_entry_point("supervisor")
        workflow.add_edge("supervisor", END)
        self.app = workflow.compile()
