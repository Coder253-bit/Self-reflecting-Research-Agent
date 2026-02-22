from typing import TypedDict, Sequence, Annotated, Optional, List 
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage, BaseMessage
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langgraph.graph import StateGraph, START, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import add_messages
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# from langchain_core.tools import tool
import os
load_dotenv()

class LLM_Model:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
    def get_structured_output(self, schema):
        return self.llm.with_structured_output(schema)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]  # all types of messages from the Human, AI, etc. 
    plan: List[str]
    research: dict
    human_feedback: Optional[str] = None
    final_report: Optional[dict]
    accuracy_report: Optional[dict]
    revision_score: int


