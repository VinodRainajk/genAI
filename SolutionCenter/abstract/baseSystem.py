from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any
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

    def __init__(self):
        """
        Initializes the system. The description is accessed from the class-level DESCRIPTION attribute.
        """
        self._tools: Dict[str, BaseTool] = {}  # Tool name -> BaseTool object

    @abstractmethod
    def add_tool(self, tool: BaseTool):
        """
        Abstract method to register a tool with the system.  Accepts a BaseTool instance.
        """
        if not isinstance(tool, BaseTool):
            raise TypeError("Tool must be an instance of BaseTool.")
        self._tools[tool.Tool_Name] = tool # Use tool.NAME as the key


    def get_all_tools_with_descriptions(self) -> List[Tuple[str, str]]:
        """
        Abstract method to get a list of all tools and their descriptions.
        Returns a list of (tool_name, tool_description) tuples.
        """
        return [(tool.Tool_Name, tool.Tool_Description) for tool in self._tools.values()]

    @abstractmethod
    def run_tool(self, tool: BaseTool, *args: Any, **kwargs: Any) -> Any:
        """
        Abstract method to run a specific tool (implementation-dependent). Accepts a BaseTool instance.
        """
        pass

    def get_system_description(self) -> str:
        """
        Method to retrieve the system's description.
        """
        return self.System_Description # Access the class-level System_Description