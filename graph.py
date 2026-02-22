from langgraph.graph import StateGraph, END, START
from agent import LLM_Model, AgentState
from nodes import *

graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)
graph.add_node("reflector", reflector_node)
graph.add_node("router", router_node)
graph.add_node("increment_revision", increment_revision_node)

graph.add_edge(START,"planner")
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", "reflector")
graph.add_edge("increment_revision", "writer")
graph.add_edge("router", END)



graph.add_conditional_edges(
    "reflector",
    router_node,
    {
        "revise": "increment_revision",
        "end": END
    }
)

app = graph.compile()

graph_without_reflection = StateGraph(AgentState)
graph_without_reflection.add_node("planner", planner_node)
graph_without_reflection.add_node("researcher", researcher_node)
graph_without_reflection.add_node("writer", writer_node)
graph_without_reflection.add_edge(START,"planner")
graph_without_reflection.add_edge("planner", "researcher")
graph_without_reflection.add_edge("researcher", "writer")
graph_without_reflection.add_edge("writer", END)

app_without_reflection = graph_without_reflection.compile()