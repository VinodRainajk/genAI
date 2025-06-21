import os
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI

from LinkednAgent.tools import get_profile_url_tavily

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if  __name__ == "__main__":
    print("hello World")
    llm_model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=google_api_key,
            temperature=0.1,
        )

    summary_Template = """
          given the full name {information} of a person I want you to give me their linkedin profile
          """
    data = "Vinod Raina Oracle"
    prompt_template = PromptTemplate.from_template(summary_Template)
    input_variables = {"information": data}

    tools_for_agent = [
        Tool(
            name = "Crawl google for linkedin Profile",
            func=get_profile_url_tavily,
            description= "useful for when you need to get the linkedin page url"
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm_model, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    result = agent_executor.invoke(
        input={"input": prompt_template.format(**input_variables)}
    )
    linked_profile_url = result["output"]
    print(linked_profile_url)
