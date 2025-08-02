from dotenv import  load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END,MessageGraph

from SolutionCenter.llmTools.systemChains import System_Identification_prompt

load_dotenv()
graph = MessageGraph()

GENERATE =  "generate"

def generate_node(state):
    print("Entering GENERATE node")
    return System_Identification_prompt.invoke({
        "messages" : state
    })

graph.add_node(GENERATE,generate_node)
graph.set_entry_point(GENERATE)

app = graph.compile()

inputs = [HumanMessage(content="Find me the system that can give me the status of card 123 456 789")]
result = app.invoke(inputs)
print(result)

# Extract the AIMessage content
if result and isinstance(result, list) and len(result) > 0:
    last_message = result[-1]  # Get the last message in the list
    if isinstance(last_message, AIMessage):
        ai_output = last_message.content
        print(ai_output)
    else:
        print("Last message is not an AIMessage.")
else:
    print("Result is empty or not in the expected format.")