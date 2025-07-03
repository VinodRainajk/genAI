from dotenv import  load_dotenv
from langchain.evaluation.comparison.prompt import SYSTEM_MESSAGE
from langgraph.graph import MessagesState
from react import llm_model,tools
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage
load_dotenv()

SYSTEM_MESSAGE = """
You are a helpful assistant that MUST use tools to answer questions.  You have access to tools, including a search engine.  If you do not know the answer to a question, ALWAYS use a tool to find the answer. You MUST always use the tools given to you to satisfy the user's request.
"""

def run_agent_reasoning(state: MessagesState)-> MessagesState:
    """
    Run the agent reasoning node.
    """
    messages = [{"role" : "system","content": SYSTEM_MESSAGE} , *state["messages"]]
    print("LLM INPUT:\n", messages)  # See what's being sent
    response: BaseMessage = llm_model.invoke(messages)
    print("LLM OUTPUT:\n", response) # See what's returned
    return{"messages":[response]}

tool_node = ToolNode(tools)