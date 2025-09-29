from langchain_core.messages import AIMessage, HumanMessage

from SolutionCenter.abstract.toolRegistration import System_Map
from SolutionCenter.llmTools.llmCall import LLM_MODEL
from SolutionCenter.llmTools.systemChains import System_Identification_prompt
from SolutionCenter.llmTools.toolChain import create_tools_identification_prompt
import json
import re  # Import the regular expression module

class OperationInfo:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):  # For easy string representation
        return f"OperationInfo(name='{self.name}', description='{self.description}')"


def system_node(state):
    print("Entering SYSTEM_IDENTIFY node")
    messages = state  # The state IS the list of messages
    print(f"messages  : {messages}")
    response = System_Identification_prompt.invoke({"messages": messages})
    print(f"response  : {response}")
    if isinstance(response, AIMessage):
        system_name = response.content.strip()  # remove leading/trailing spaces
        # Append the response of the System identification to the list of messages
        messages.append(AIMessage(content=f"Identified system: {system_name}"))

        return messages  # pass the messages (which is the state)
    else:
        raise ValueError(
            "Unexpected response type from system identification chain: {}".format(
                type(response)
            )
        )


def tool_extract_node(state):
    print("Entering TOOL_EXTRACT node")

    messages = state  # The state IS the list of messages

    # Get the JSON response from the last message
    json_response = messages[-1].content.replace("Identified system: ", "") # assuming the json response is after "Identified system: "
    print(f"JSON Response: {json_response}")
    # Remove any surrounding text, including markdown formatting (```json ... ```)
    json_response = re.sub(r'^(.*?)```json\n', '', json_response)  # Remove anything before ```json
    json_response = re.sub(r'\n```(.*?)$', '', json_response)  # Remove anything after ```
    json_response = json_response.replace("Identified system: ", "").strip()  # Remove prefix and whitespace


    print(f"Cleaned JSON Response: {json_response}")

    if not json_response:
        raise ValueError("JSON response not found in state.")

    try:
        data = json.loads(json_response)
        #systems = data.get("systems")
        systems = data
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")
    except AttributeError as e:
        raise ValueError(f"Attribute Error: {e}")


    if not systems:
        raise ValueError("No 'systems' found in JSON response.")

    # Create a list to store OperationInfo objects
    operation_info_list = []

    # Iterate through the systems and create OperationInfo objects
    for system in systems:
        system_name = system.get("systemName")
        description = system.get("description")

        if system_name and description:  # Ensure both values exist
            operation_info = OperationInfo(system_name, description)
            operation_info_list.append(operation_info)
        else:
            print(f"Skipping system due to missing systemName or description: {system}") #Log skipped

    print(f"operation_info_list: {operation_info_list}")
    # Add the list to messages
    messages.append(AIMessage(content=f"Tools List: {operation_info_list}"))  # Pass the whole list
    return messages


def tool_Conditional_Parser(state):
    print("Entering TOOL_CONDITIONAL_PARSER node")
    messages = state
    system_description_list_str = messages[-1].content.replace("Tools List: ", "")
    operation_info_list = eval(system_description_list_str)
    query_and_result = ""
    while operation_info_list:
        operation_info = operation_info_list[0]
        operation_info_list = operation_info_list[1:]
        messages[-1] = AIMessage(content=f"Tools List: {operation_info_list}")

        system_name = operation_info.name
        print(f"operation_info --> {operation_info}")
        if system_name in System_Map:
            system_details = System_Map[system_name]
            tools_description = system_details.get_all_tools_with_descriptions()
            actual_query_to_be_processed = operation_info.description
            tools_description_with_context = ""
            if query_and_result:
                tools_description_with_context = f"{operation_info.description}. Tools: {tools_description}. Additional query results {query_and_result}"
            else:
                tools_description_with_context = f"{operation_info.description}. Tools: {tools_description}"

            try:
                tool_info = tool_identify_node(tools_description_with_context)
                result = tool_execution_node(tool_info)
                print(f"result of the Tool Execution is {result}")
                query_and_result = f"Executed the query {actual_query_to_be_processed} and got result {result}"
                print(f"{query_and_result}")
                messages.append(AIMessage(content=f"For the query {actual_query_to_be_processed} and got result {result}"))
            except Exception as e:
                messages.append(AIMessage(content=f"Error during tool identification or execution: {e}"))
        else:
            print(f"System '{system_name}' not found in System_Map.")
            messages.append(AIMessage(content=f"System '{system_name}' not found in System_Map."))

    print("All operations processed.")
    return messages


def tool_identify_node(request):
    print("Entering TOOL_IDENTIFY function") #Note it is not a node anymore

    print(f"Request to TOOL_IDENTIFY: {request}")
    if not request:
        raise ValueError("Tools not found in state.")

    # Use the extracted tool names to invoke the Tools_Identification_prompt
    tools_identification_prompt = create_tools_identification_prompt(request)
    chain = tools_identification_prompt | LLM_MODEL

    # Wrap the request in a HumanMessage and pass it as a list
    message = HumanMessage(content=request)
    response = chain.invoke({"messages": [message]})

    print(f"TOOL_IDENTIFY function output: {response}")

    # Extract JUST the tool name (You'll need to adjust this based on your LLM's output format)
    # Assuming the LLM returns something like "Tool: CreditCardStatus"
    full_response = response.content
    if "**" in full_response:
        tool_name = full_response.split("**")[1]  # Extract text between the **
        # Extract parameters (This is a placeholder.  You'll need to refine this based on your LLM output)
        parameters = {}  # Or extract from the LLM output if it provides them
    else:
        tool_name = full_response  # if no ** just return the full response
        parameters = {} #default
    tool_name = tool_name.strip()  # Remove any extra spaces

    # Create JSON
    tool_info = {"tool_name": tool_name, "parameters": parameters}
    return tool_info


import json
import re

def tool_execution_node(tool_info):
    print("Entering TOOL_EXECUTION function")
    print(f"tool_info: {tool_info}")

    try:
        # Extract the JSON string and remove the surrounding ```json\n and \n```
        json_string = tool_info["tool_name"].replace("```json\n", "").replace("\n```", "")

        # Parse the cleaned JSON string
        tool_info_parsed = json.loads(json_string)
        tool_name = tool_info_parsed["tool_name"]
        parameters = tool_info_parsed["parameters"]
    except (KeyError, json.JSONDecodeError) as e:
        return f"Error extracting data from JSON: {e}"

    print(f"Tool name: {tool_name}")
    print(f"Parameters: {parameters}")

    # Find the tool in the System_Map
    for system_name, system in System_Map.items():
        tool = system.get_tool(tool_name)  # Assuming you have a get_tool method
        if tool:
            break
    else:
        return f"Tool '{tool_name}' not found in System_Map."

    # Execute the tool
    try:
        result = tool.execute(parameters)  # Pass parameters to the execute function
        print(f"Tool '{tool_name}' executed successfully.")
        print(f"result {result}")
        return result
    except Exception as e:
        return f"Error executing tool '{tool_name}': {e}"