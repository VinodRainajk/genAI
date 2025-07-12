import os
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import  load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
generation_prompt =  ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a twitter techie influencer assistant tasked with wirting excellent twitter posts."
         " generate the best twitter post possible for the user's request."
         " If the user provides critique, respond with a revised version of your previous attempts. ",
         ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "you are a virual twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
         "Alwats provice detailed recommendations, including requests for length, virality, style, etc",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=google_api_key,
    temperature=0.1,
)
generation_chain = generation_prompt| llm_model
reflection_chain = reflection_prompt|llm_model
