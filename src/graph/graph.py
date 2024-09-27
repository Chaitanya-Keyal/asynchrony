from langgraph.graph import END, StateGraph

from src.graph import Nodes, State


class Workflow:
    def __init__(self):
        self.supervisor_edges = {
            "customer-expert": "customer_expert",
            "transaction-expert": "transaction_expert",
            "complaints-expert": "complaints_expert",
        }

        def supervisor_edge(state):
            return self.supervisor_edges[state.get("agent_output")["output"]]

        nodes = Nodes()
        workflow = StateGraph(State)
        workflow.add_node("supervisor", nodes.supervisor)
        workflow.add_node("transaction_expert", nodes.transaction_expert)
        workflow.add_node("customer_expert", nodes.customer_expert)
        workflow.add_node("complaints_expert", nodes.complaints_expert)
        workflow.set_entry_point("supervisor")
        workflow.add_conditional_edges("supervisor", supervisor_edge)
        workflow.add_edge("transaction_expert", END)
        workflow.add_edge("customer_expert", END)
        workflow.add_edge("complaints_expert", END)
        self.app = workflow.compile()
