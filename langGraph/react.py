from dotenv import  load_dotenv
import requests
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI
from geopy.geocoders import Nominatim
load_dotenv()
import os
from bs4 import BeautifulSoup
import json

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
geolocator = Nominatim(user_agent="weather-app")

@tool(description="Triples the input number and then returns it")
def triple(num : float) -> float:
    """
    param num: a number to triple
    returns:  the triple of the input number
    """

    return float(num)*3

tools = [triple , TavilySearch(max_results=1, tavily_api_key=tavily_api_key)]

llm_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key,
        temperature=0.1,
    ).bind_tools(tools)