from SolutionCenter.abstract.systemDefinition.cards.cardSystem import CardsSystem
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCardStatus import CurrentCardStatus
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCreditLimit import CurrentCreditLimit

currentCardStatus_tool = CurrentCardStatus()
cardSystem = CardsSystem()
cardSystem.add_tool(currentCardStatus_tool)
cardSystem.add_tool(CurrentCreditLimit())

print("Card All Tool Description is -->",cardSystem.get_all_tools_with_descriptions())
print( cardSystem.get_tool("CreditCardLimit").execute("1"))