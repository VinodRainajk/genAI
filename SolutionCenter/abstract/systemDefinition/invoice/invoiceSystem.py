from typing import Any

from SolutionCenter.abstract.baseSystem import BaseSystem
from SolutionCenter.abstract.baseTool import BaseTool


class InvoiceSystem(BaseSystem):

    System_Description_Value = (" This system is containing the details of invoices. The Main operations that can be performed here is that user will be able to:"
                                "1: find the status of Invoice"
                                "2: get the invoice amount "
                                "3: where is the invoice pending for approval")

    System_Name_value = "Invoice"

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

    @property
    def System_Name(self) -> str:
        return self.__class__.System_Name_value