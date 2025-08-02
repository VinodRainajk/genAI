from SolutionCenter.abstract.baseTool import BaseTool


class PaymentStatus(BaseTool):
    Tool_Name_Value  = "PaymentStatus"
    Tool_Description_Value  = ("This tool will provide current status of the payment on Invoice ")

    def __init__(self):
        super().__init__()

    def execute(self) -> str:
        """
        Example implementation of the execute method.
        """
        return "Payment is pending at person Y"

    @property
    def Tool_Name(self) -> str:
        return self.__class__.Tool_Name_Value

    @property
    def Tool_Description(self) -> str:
        return self.__class__.Tool_Description_Value