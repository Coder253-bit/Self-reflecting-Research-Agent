import warnings
warnings.filterwarnings("ignore")
from agent import LLM_Model, AgentState
from tools import Tools
from pydantic import BaseModel, Field
from typing import List
from langgraph.graph import add_messages
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage, BaseMessage
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from dataclasses import dataclass  



agentstate = AgentState()
llm_chat_model = LLM_Model()
tools = Tools()

class Plan(BaseModel): 
    """Plan to follow for user query"""
    steps: List[str] = Field(description="different steps to take, should be in priority order")


planner_llm = llm_chat_model.get_structured_output(Plan)
planner_prompt = ChatPromptTemplate.from_template(
    "For the following input, come up with a list of 2 relevant topics to search for. "
    "Include most relevant topics in order of priority.\n\n{input}")

def planner_node(state: agentstate):
    """Generates an initial plan for the user query"""
    if not state["messages"]:
        raise ValueError("No user message found in state.")
    user_query = state["messages"][-1].content
    planner_chain = planner_prompt | planner_llm
    plan = planner_chain.invoke({"input": user_query})  # Passing into the LLM, the last user's question
    return {"plan": plan.steps}

def researcher_node(state: agentstate):
    """Executes the web search for each topic in the plan."""

    # storing the research results in a clean dictionary
    research_results = {}
    for topic in state["plan"]:
        result = tools.research_tool(topic)
        research_results[topic] = result
    
    return {"research": research_results}


class FinalReport(BaseModel):
    title: str
    summary: str
    source: str


def writer_node(state: agentstate):
    """Writes the output cleanly from the given research dictionary"""

    writer_llm = llm_chat_model.get_structured_output(FinalReport)
    research_data = state["research"]
    feedback = ""
    if state.get("accuracy_report"):
        feedback = state["accuracy_report"]["feedback"]

    result = writer_llm.invoke(
    f"""Write a structured report with a title, summary and URL combining research from research: {research_data} and feedback: {feedback} (if any). 
    Ensure:
    - title
    - summary 
    - URL
    The information does not exceed 70 words total.
    If feedback is present, you MUST correct every issue mentioned in feedback.
    """)

    return {"final_report": result.dict()}

class AccuracyReport(BaseModel):
    feedback: str
    score: int = Field(description="should be in range of 1-10")

def reflector_node(state: agentstate):
    reflector_llm = llm_chat_model.get_structured_output(AccuracyReport)
    final_report = state["final_report"]
    result = reflector_llm.invoke(
        f"""
        Evaluate this report:

        {final_report}

        Criteria:
        - factual accuracy
        - missing info
        - clarity
        - relevance
        List exactly what is missing. Be specific.

        Provide:
        - feedback (max 20 words)
        - score (1-10)
        """
        )
    return {
    "accuracy_report": result.dict(),
    "revision_score": state.get("revision_score", 0)
        }

def router_node(state: agentstate) -> agentstate:
    accuracy_score = state["accuracy_report"]["score"]
    revision_score = state.get("revision_score", 0)
    if accuracy_score < 8 and revision_score < 2:
        return "revise"
    else:
        return "end" 

def increment_revision_node(state: AgentState):
    return {"revision_score": state["revision_score"] + 1}


