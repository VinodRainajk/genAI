# toolChain.py
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


def create_tools_identification_prompt(tool_descriptions):
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an intelligent Support center person with the following tools at your disposal:\n"
                + tool_descriptions
                + "You have to identify which system is best suited to respond to the query, you need to provide the system name that will be used.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )


LLM_MODEL = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", google_api_key=google_api_key, temperature=0.1
)