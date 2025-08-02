import os
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import  load_dotenv

from SolutionCenter.abstract.systemDefinition.cards.cardSystem import CardsSystem
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCardStatus import CurrentCardStatus
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCreditLimit import CurrentCreditLimit
from SolutionCenter.abstract.systemDefinition.invoice.invoiceSystem import InvoiceSystem
from SolutionCenter.abstract.systemDefinition.invoice.tools.invoiceStatus import InvoiceStatus
from SolutionCenter.abstract.systemDefinition.invoice.tools.paymentStatus import PaymentStatus

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")



# --- Instantiate the tools ---
card_system = CardsSystem()
invoice_system = InvoiceSystem()

card_system.add_tool(CurrentCardStatus())
card_system.add_tool(CurrentCreditLimit())
invoice_system.add_tool(InvoiceStatus())
invoice_system.add_tool(PaymentStatus())

# --- Build the tool list information string ---
system_list_info = ""  # Initialize as empty string
system_list_info += (
    f"Tool Name: {card_system.System_Name}, Description: {card_system.System_Description}\n"
)
system_list_info += f"Tool Name: {invoice_system.System_Name}, Description: {invoice_system.System_Description}\n"

System_Identification_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an intelligent Support center person with the following tools at your disposal:\n"
            + system_list_info
            + "You have to identify which system is best suited to respond to the query, you need to provide the system name that will be used.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=google_api_key,
    temperature=0.1,
)
System_Identification_prompt = System_Identification_prompt| llm_model

