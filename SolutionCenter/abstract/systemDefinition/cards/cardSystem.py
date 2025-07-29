from typing import Any

from SolutionCenter.abstract.baseSystem import BaseSystem
from SolutionCenter.abstract.baseTool import BaseTool


class CardsSystem(BaseSystem):

    System_Description_Value = (" This system is containing the details of credit Cards. The main operations that are releated to Credit card"
                          "like inqury about the status of Credit card, if the card is blocked, If the card is expired, status of new credit cards. "
                          "Address where it will be delivered, "
                          "Limit of the current credit card ,"
                          "When the new Credit Card will be delivered will be answered by this system")

    def __init__(self):
        super().__init__()


    def run_tool(self, tool: BaseTool, *args: Any, **kwargs: Any) -> Any:
        """
        Executes the given tool.
        """
        if not isinstance(tool, BaseTool):
            raise TypeError("tool must be an instance of BaseTool")
        return tool.execute(*args, **kwargs)

    @property
    def System_Description(self) -> str:
        return self.__class__.System_Description_Value  # Access the class attribute