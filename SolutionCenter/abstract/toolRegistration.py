from SolutionCenter.abstract.systemDefinition.cards.cardSystem import CardsSystem
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCardStatus import CurrentCardStatus
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCreditLimit import CurrentCreditLimit
from SolutionCenter.abstract.systemDefinition.invoice.invoiceSystem import InvoiceSystem
from SolutionCenter.abstract.systemDefinition.invoice.tools.invoiceStatus import InvoiceStatus

cardSystem = CardsSystem()
cardSystem.add_tool(CurrentCardStatus())
cardSystem.add_tool(CurrentCreditLimit())

invoiceSystem = InvoiceSystem()
invoiceSystem.add_tool(InvoiceStatus())


print("Card All Tool Description is -->",cardSystem.get_all_tools_with_descriptions())
print("Card All Tool Description is -->",cardSystem.get_system_description())
print( cardSystem.get_tool("CreditCardLimit").execute("1"))

systems = {
    cardSystem.get_system_Name(): cardSystem,
    invoiceSystem.get_system_Name(): invoiceSystem,
}

# Iterate through the dictionary and print the system names and descriptions
for system_name, system_object in systems.items():
    print(f"System Name: {system_name}")
    print(f"System Description: {system_object.get_system_description()}")
    print(f"Tool list: {system_object.get_all_tools_with_descriptions()}")
    print("-" * 20)