from SolutionCenter.abstract.baseTool import BaseTool


class CurrentCreditLimit(BaseTool):
    Tool_Name_Value  = "CreditCardLimit"
    Tool_Description_Value  = ("This tool will help you check the limit of the Credit Card.")

    def __init__(self):
        super().__init__()

    def execute(self,args1: str) -> str:
        """
        Example implementation of the execute method.
        """
        return "Card limit is 1 Million"

    @property
    def Tool_Name(self) -> str:
        return self.__class__.Tool_Name_Value

    @property
    def Tool_Description(self) -> str:
        return self.__class__.Tool_Description_Value