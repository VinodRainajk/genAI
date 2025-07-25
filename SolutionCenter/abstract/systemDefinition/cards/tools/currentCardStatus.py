from SolutionCenter.abstract.baseTool import BaseTool

class CurrentCardStatus(BaseTool):
    Tool_Name = "CreditCardStatus"
    Tool_Description = ("This tool will identify the current status of the credit card.")

    def __init__(self):
        super().__init__()

    def execute(self, arg1: int) -> str:
        """
        Example implementation of the execute method.
        """
        return "Card is currently blocked"

    @property
    def Tool_Name(self) -> str:
        return self.__class__.Tool_Name

    @property
    def Tool_Description(self) -> str:
        return self.__class__.Tool_Description