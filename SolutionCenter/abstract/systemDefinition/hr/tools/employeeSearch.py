from SolutionCenter.abstract.baseTool import BaseTool

class EmployeeSearch(BaseTool):
    Tool_Name_Value  = "employeeSearch"
    Tool_Description_Value  = ("This tool will help you find the employee id based on employee email id, so email ID should be passed as a paremeter to execute method")

    def __init__(self):
        super().__init__()

    def execute(self, employee_email: str) -> str:
        """
        Fetches employee ID based on the provided email.
        You would typically query your data source here.
        """
        # Placeholder logic — replace with actual database lookup
        mock_employee_db = {
            "alice@example.com": "2001561",
            "bob@example.com": "2001562",
            "vinod@example.com": "2001563"
        }
        employee_id = mock_employee_db.get(employee_email)
        if employee_id:
            return employee_id
        else:
            raise ValueError(f"No employee ID found for email: {employee_email}")

    @property
    def Tool_Name(self) -> str:
        return self.__class__.Tool_Name_Value

    @property
    def Tool_Description(self) -> str:
        return self.__class__.Tool_Description_Value