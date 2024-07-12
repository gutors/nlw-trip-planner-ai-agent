import os
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
)

tools = load_tools(['ddg-search', 'wikipedia'], llm = llm)

prompt = hub.pull("hwchase17/react")

# print(tools[0].name, tools[0].description)
# print(tools[1].name, tools[1].description)

# create a reAct agent (reason and act)
agent = create_react_agent(llm, tools, prompt)

agentExecutor = AgentExecutor(agent=agent, tools=tools, prompt=prompt, verbose='true')

#print(agent.agent.llm_chain.prompt.template)

query="""
Vou viajar para Asia em Agosto de 2024. Quero que faça um roteiro com os eventos que vao ocorrer na data da viagem e o preco das passagens de Sao Paulo para Tailandia.
"""

agentExecutor.invoke({"input":query})