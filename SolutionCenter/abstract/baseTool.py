from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any

class BaseTool(ABC):
    """
    Abstract base class for tools.
    The tool name and description are defined as class attributes in concrete subclasses.
    """

    @property
    @abstractmethod
    def Tool_Name(self) -> str:
        """
        Abstract property that *must* be overridden in subclasses to provide the tool's name.
        """
        pass

    @property
    @abstractmethod
    def Tool_Description(self) -> str:
        """
        Abstract property that *must* be overridden in subclasses to provide the tool's description.
        """
        pass

    def __init__(self):
        """
        Initializes the tool. The name and description are accessed from the class-level attributes.
        """
        pass #No initialization is needed

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """
        Abstract method to execute the tool's functionality.  Accepts any number of arguments.
        """
        pass

    def get_tool_description(self) -> str:
        """
        Method to retrieve the system's description.
        """
        return self.Tool_Description # Access the class-level System_Description