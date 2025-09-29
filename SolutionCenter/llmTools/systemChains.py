import os
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import  load_dotenv
from SolutionCenter.abstract.toolRegistration import System_List_Info


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

System_Identification_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an intelligent Support center person with the following tools at your disposal:\n"
            + System_List_Info
            + "Thought : You have to check the query that user has input and validate it against the list of system that are provided"
            + "Read the description of the system and the operation it performs, do not conclude immediately"
            + "Action: Identify which system is best suited to respond to the query, you need to provide the system name that will be used."
            + "If there are multiple system that needs to be executed then you will have to return the list of system along with description of the actions that needs to be performed"
            + "Response should be in a  List of Json format with system  name and Description of the task to be performed, so that It can be parsed easily"
            + "If there are multiple system Involved then the response should be a single JSON file with List of JSON each containing the systemName and Description",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm_model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=google_api_key,
    temperature=0.1,
)
System_Identification_prompt = System_Identification_prompt| llm_model

