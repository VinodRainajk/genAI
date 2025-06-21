from tempfile import template
from typing import Union, List
import json
from click import prompt
from dotenv import load_dotenv
from langchain.tools import Tool, tool
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain_core.agents import AgentFinish, AgentAction
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import render_text_description
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor
import os

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Returns the length of text by Characters"""
    text = text.strip("'\n'").strip('"')
    print(f"inside the get_text_length")
    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")

import json

def parse_llm_response(response_content):
    """Parses the LLM response and extracts relevant information."""

    # Split the content into segments
    segments = response_content.split('\n')

    parsed_data = {}

    for segment in segments:
        if ":" in segment:
            key, value = segment.split(":", 1)  # Split only on the first colon
            parsed_data[key.strip()] = value.strip()

    return {
        "question": parsed_data.get("Question"),
        "thought": parsed_data.get("Thought"),
        "action": parsed_data.get("Action"),
        "action_input": parsed_data.get("Action Input"),
        "observation": parsed_data.get("Observation"),
        "final_answer": parsed_data.get("Final Answer"),
    }



google_api_key = os.getenv("GOOGLE_API_KEY")
if __name__ == '__main__':
    print('Hello React LangChain')
    toolsList = [get_text_length]
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:
    """

    prompt = PromptTemplate.from_template(template=template).partial(tools=render_text_description(toolsList),
                                                                     tool_names=" , ".join([t.name for t in toolsList]))

    llm_model = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=google_api_key,
        temperature=0.1,
    )


    agent = {"input": lambda x:x ["input"]} | prompt | llm_model
    agent_step = agent.invoke({"input" : "What is the text length of 'DOG' in characters?'"})
    print(agent_step)
    response  = parse_llm_response(agent_step.content)
    print(response)
    tool_to_use =  find_tool_by_name(toolsList,response.get('action'))
    print(tool_to_use)
    observation = tool_to_use.func(str(response.get('action_input')))
    print(observation)


