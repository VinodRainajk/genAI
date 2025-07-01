from dotenv import  load_dotenv
from langchain.evaluation.comparison.prompt import SYSTEM_MESSAGE
from langgraph.graph import MessagesState

from pyexpat.errors import messages
from langgraph.prebuilt import ToolNode
from langGraph.react import tools
from react import llm_model,tool

load_dotenv()

SYSTEM_MESSAGE = """
You are a helpful assistant that can use tools to answer questions
"""

def run_agent_reasoning(state: MessagesState)-> MessagesState:
    """
    Run the agent reasoning node.
    """
    response = llm_model.invoke([{"role" : "system","content": SYSTEM_MESSAGE} , *state["messages"]])
    return{"messages":[response]}

tool_node = ToolNode(tools)