from SolutionCenter.abstract.systemDefinition.cards.cardSystem import CardsSystem
from SolutionCenter.abstract.systemDefinition.cards.tools.currentCardStatus import CurrentCardStatus

currentCardStatus_tool = CurrentCardStatus()
cardSystem = CardsSystem()
cardSystem.add_tool(currentCardStatus_tool)

print("Card Description is ")
print( cardSystem.get_system_description())