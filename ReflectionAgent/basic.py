from dotenv import  load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END,MessageGraph
from chains import generation_chain,reflection_chain

load_dotenv()
graph = MessageGraph()

REFLECT = "reflect"
GENERATE =  "generate"

def generate_node(state):
    print("Entering GENERATE node")
    return generation_chain.invoke({
        "messages" : state
    })

def reflect_node(state):
    print("Entering REFLECT node")
    response = reflection_chain.invoke({
        "messages" : state
    })
    print(f"REFLECT node output: {response}")
    return [HumanMessage(content=response.content)]



graph.add_node(GENERATE,generate_node)
graph.add_node(REFLECT,reflect_node)
graph.set_entry_point(GENERATE)

def should_continue(state):
    print("Checking should_continue condition")  # Debugging print
    if len(state) > 4:
        print("should_continue: END")  # Debugging print
        return END
    else:
        print("should_continue: REFLECT")  # Debugging print
        return REFLECT

graph.add_conditional_edges(GENERATE,should_continue)
graph.add_edge(REFLECT,GENERATE)

app = graph.compile()

inputs = [HumanMessage(content="Tell me a joke.")]
result = app.invoke(inputs)
print(result)