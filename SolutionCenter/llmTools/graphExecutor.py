from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import MessageGraph

from SolutionCenter.llmTools.graphNodes import system_node, tool_extract_node, tool_identify_node, tool_execution_node, \
    tool_Conditional_Parser

load_dotenv()

graph = MessageGraph()

SYSTEM_IDENTIFY = "system_identify"  # Rename for clarity
TOOL_EXTRACT = "tool_extract"
TOOL_IDENTIFY = "tool_identify"
TOOL_EXECUTION= "tool_execution"
TOOL_CONDITON = "tool_Conditional_Parser"
# Add the nodes to the graph
graph.add_node(SYSTEM_IDENTIFY, system_node)
graph.add_node(TOOL_EXTRACT, tool_extract_node)
graph.add_node(TOOL_CONDITON, tool_Conditional_Parser)


# Define the edges
graph.add_edge(SYSTEM_IDENTIFY, TOOL_EXTRACT)
graph.add_edge(TOOL_EXTRACT, TOOL_CONDITON)
#graph.add_edge(TOOL_IDENTIFY,TOOL_EXECUTION)

graph.set_entry_point(SYSTEM_IDENTIFY)  # Start at the system identification node

app = graph.compile()
app.get_graph().draw_mermaid_png(output_file_path="flow.png")

inputs = [
    HumanMessage(content="Find me the card limit id of employee with employee who has email id vinod@example.com")
]

result = app.invoke(inputs)  # Pass the list of messages directly
print(result)