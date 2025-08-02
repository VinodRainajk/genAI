from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessageGraph

from SolutionCenter.abstract.toolRegistration import System_Map
from SolutionCenter.llmTools.llmCall import LLM_MODEL
from SolutionCenter.llmTools.systemChains import System_Identification_prompt
from SolutionCenter.llmTools.toolChain import create_tools_identification_prompt

load_dotenv()


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
    return response  # Return the final response from the tool identification chain


graph = MessageGraph()

SYSTEM_IDENTIFY = "system_identify"  # Rename for clarity
TOOL_EXTRACT = "tool_extract"
TOOL_IDENTIFY = "tool_identify"
# Add the nodes to the graph
graph.add_node(SYSTEM_IDENTIFY, system_node)
graph.add_node(TOOL_EXTRACT, tool_extract_node)
graph.add_node(TOOL_IDENTIFY, tool_identify_node)

# Define the edges
graph.add_edge(SYSTEM_IDENTIFY, TOOL_EXTRACT)
graph.add_edge(TOOL_EXTRACT, TOOL_IDENTIFY)

graph.set_entry_point(SYSTEM_IDENTIFY)  # Start at the system identification node

app = graph.compile()

inputs = [
    HumanMessage(content="Find me the system that can give me the status of card 123 456 789")
]

result = app.invoke(inputs)  # Pass the list of messages directly
print(result)