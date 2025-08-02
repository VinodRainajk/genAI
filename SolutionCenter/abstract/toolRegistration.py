# --- Instantiate the tools ---
from SolutionCenter.abstract.systemDefinition.cards.cardSystem import CardsSystem
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCardStatus import CurrentCardStatus
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCreditLimit import CurrentCreditLimit
from SolutionCenter.abstract.systemDefinition.invoice.invoiceSystem import InvoiceSystem
from SolutionCenter.abstract.systemDefinition.invoice.tools.invoiceStatus import InvoiceStatus
from SolutionCenter.abstract.systemDefinition.invoice.tools.paymentStatus import PaymentStatus

card_system = CardsSystem()
invoice_system = InvoiceSystem()

card_system.add_tool(CurrentCardStatus())
card_system.add_tool(CurrentCreditLimit())
invoice_system.add_tool(InvoiceStatus())
invoice_system.add_tool(PaymentStatus())

# --- Build the tool list information string ---
System_List_Info = ""  # Initialize as empty string
System_List_Info += (
    f"Tool Name: {card_system.System_Name}, Description: {card_system.System_Description}\n"
)
System_List_Info += f"Tool Name: {invoice_system.System_Name}, Description: {invoice_system.System_Description}\n"


System_Map = {
    card_system.System_Name: card_system,
    invoice_system.System_Name: invoice_system,
}