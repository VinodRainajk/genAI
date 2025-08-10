from SolutionCenter.abstract.baseTool import BaseTool


class CurrentCreditLimit(BaseTool):
    Tool_Name_Value  = "CreditCardLimit"
    Tool_Description_Value  = ("This tool will help you check the limit of the Credit Card for the employee nased on employee id. You will hae to provide employee id as the parameter")

    def __init__(self):
        super().__init__()

    def execute(self, parameters: dict) -> str:
        """
        Fetches employee ID based on the provided email.
        You would typically query your data source here.
        """
        # Extract the email from the parameters dictionary
        employee_employeeid = parameters.get('employee_id')  # Use .get() to avoid KeyError

        if not employee_employeeid:
            raise ValueError("employee_id not provided in parameters")

        # Placeholder logic — replace with actual database lookup
        mock_card_db = {
            "2001561": "10000",
            "2001562": "20000",
            "2001563": "64646"
        }
        card_limit = mock_card_db.get(employee_employeeid)  # Use the email to look up the employee ID
        if card_limit:
            return card_limit
        else:
            raise ValueError(f"No employee ID found for email: {employee_employeeid}")

    @property
    def Tool_Name(self) -> str:
        return self.__class__.Tool_Name_Value

    @property
    def Tool_Description(self) -> str:
        return self.__class__.Tool_Description_Value