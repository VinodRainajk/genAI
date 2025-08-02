from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional
from SolutionCenter.abstract.baseTool import BaseTool


class BaseSystem(ABC):
    """
    Abstract base class for systems.
    The system description is defined as a class attribute in concrete subclasses.
    """

    @property
    @abstractmethod
    def System_Description(self) -> str:
        """
        Abstract property that *must* be overridden in subclasses to provide the system description.
        """
        pass  # This should *not* be assigned a default value in the base class

    @property
    @abstractmethod
    def System_Name(self) -> str:
        """
        Abstract property that *must* be overridden in subclasses to provide the system description.
        """
        pass  # This should *not* be assigned a default value in the base class


    def __init__(self):
        """
        Initializes the system. The description is accessed from the class-level DESCRIPTION attribute.
        """
        self._tools: Dict[str, BaseTool] = {}  # Tool name -> BaseTool object


    def add_tool(self, tool: BaseTool):
        """
        Abstract method to register a tool with the system.  Accepts a BaseTool instance.
        """
        if not isinstance(tool, BaseTool):
            raise TypeError("Tool must be an instance of BaseTool.")
        self._tools[tool.Tool_Name] = tool # Use tool.NAME as the key

    def get_all_tools_with_descriptions(self) -> List[str]:
        """Returns a list of strings, where each string contains the tool name and its description."""
        tool_descriptions = []
        for tool_name, tool in self._tools.items():
            tool_descriptions.append(
                f"Tool Name: {tool_name} , Description :{tool.get_tool_description()}"
            )  # Assuming BaseTool has a get_tool_description() method
        return tool_descriptions

    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """
        Retrieves a tool by its name.

        Args:
            tool_name: The name of the tool to retrieve.

        Returns:
            The tool object if found, otherwise None.
        """
        return self._tools.get(tool_name)


    def get_system_description(self) -> str:
        """
        Method to retrieve the system's description.
        """
        return self.System_Description # Access the class-level System_Description

    def get_system_Name(self) -> str:
        """
        Method to retrieve the system's description.
        """
        return self.System_Name # Access the class-level System_Description