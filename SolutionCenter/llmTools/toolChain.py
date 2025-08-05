# toolChain.py
import os

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from SolutionCenter.abstract.toolRegistration import System_Map
from SolutionCenter.llmTools.systemChains import System_Identification_prompt

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


def create_tools_identification_prompt(tool_descriptions):
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an intelligent Support center person with the following tools at your disposal:\n"
                + tool_descriptions

                + "You have to identify which tool is best suited to respond to the query. Your response MUST be a JSON object with the following format:\n"
                + "You should have tool name and the list of paramters in the json output"
                + "If a tool requires no parameters, the  field should be an empty object: .\n"
                + "Ensure the JSON is valid and parsable. Do NOT include any text outside the JSON object.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
