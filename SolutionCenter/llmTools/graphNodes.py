from langchain_core.messages import AIMessage

from SolutionCenter.abstract.toolRegistration import System_Map
from SolutionCenter.llmTools.llmCall import LLM_MODEL
from SolutionCenter.llmTools.systemChains import System_Identification_prompt
from SolutionCenter.llmTools.toolChain import create_tools_identification_prompt


def system_node(state):
    print("Entering SYSTEM_IDENTIFY node")
    messages = state  # The state IS the list of messages

    response = System_Identification_prompt.invoke({"messages": messages})
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

    # Get the system_name from the last message of the state
    system_name = messages[-1].content.replace("Identified system: ", "")

    if not system_name:
        raise ValueError("System name not found in state.")

    system_details = System_Map.get(system_name)

    if not system_details:
        raise ValueError(f"System '{system_name}' not found in System_Map.")

    tools_description = system_details.get_all_tools_with_descriptions()

    messages.append(AIMessage(content=f"Tools Description: {tools_description}"))
    return messages


def tool_identify_node(state):
    print("Entering TOOL_IDENTIFY node")
    messages = state  # The state IS the list of messages
    tools_description = messages[-1].content.replace("Tools Description: ", "")

    if not tools_description:
        raise ValueError("Tools not found in state.")

    # Use the extracted tool names to invoke the Tools_Identification_prompt
    tools_identification_prompt = create_tools_identification_prompt(tools_description)
    chain = tools_identification_prompt | LLM_MODEL
    response = chain.invoke({"messages": messages})  # Pass the whole list of Messages

    print(f"TOOL_IDENTIFY node output: {response}")

    # Extract JUST the tool name (You'll need to adjust this based on your LLM's output format)
    # Assuming the LLM returns something like "Tool: CreditCardStatus"
    full_response = response.content
    if "**" in full_response:
        tool_name = full_response.split("**")[1]  # Extract text between the **
    else:
        tool_name = full_response  # if no ** just return the full response

    tool_name = tool_name.strip()  # Remove any extra spaces

    return [AIMessage(content=tool_name)]  # Return a LIST containing the tool name


def tool_execution_node(state):
    print("Entering TOOL_EXECUTION node")
    tool_name = state[-1].content  # Get the identified tool name
    print(f"tool_name :{tool_name}")
    # Find the tool in the System_Map
    for system_name, system in System_Map.items():
        tool = system.get_tool(tool_name)  # Assuming you have a get_tool method
        if tool:
            break
    else:
        raise ValueError(f"Tool '{tool_name}' not found in System_Map.")

    # Execute the tool
    try:
        result = tool.execute()
        print(f"Tool '{tool_name}' executed successfully.")
    except Exception as e:
        return f"Error executing tool '{tool_name}': {e}"

    return result  # Pass the result