from SolutionCenter.abstract.baseTool import BaseTool

class InvoiceStatus(BaseTool):
    Tool_Name_Value  = "InvoiceStatus"
    Tool_Description_Value  = ("This tool will provide current status of the invoice ")

    def __init__(self):
        super().__init__()

    def execute(self) -> str:
        """
        Example implementation of the execute method.
        """
        return "Invoice is at XYZ Status"

    @property
    def Tool_Name(self) -> str:
        return self.__class__.Tool_Name_Value

    @property
    def Tool_Description(self) -> str:
        return self.__class__.Tool_Description_Value
