from dotenv import  load_dotenv
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
import os

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
@tool
def triple(num : float) -> float:
    """
    param num: a number to triple
    returns:  the triple of the input number
    """

    return float(num)*3

tools = [TavilySearch(max_results=1, tavily_api_key=tavily_api_key), triple]

llm_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key,
        temperature=0.1,
    )

llm_model.bind_tools(tools)