import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores.chroma import Chroma
import bs4

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import json

OPENAI_API_KEY= os.environ['OPENAI_API_KEY']

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

# query="""
# Vou viajar para Inglaterra em Agosto de 2024. Quero que faça um roteiro com os eventos que vao ocorrer na data da viagem e o preco das passagens de Sao Paulo para Londres.
# """

def researchAgent(query: str, llm: ChatOpenAI):
    tools = load_tools(['ddg-search', 'wikipedia'], llm = llm)
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, prompt=prompt)
    webContext = agent_executor.invoke({"input":query})
    return webContext['output']

def loadData():
    loader = WebBaseLoader(
        web_path="https://dicasdeviagem.com/inglaterra",
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("postcontentwrap", "pagetitleloading background-imaged loading-dark"))),
    )
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(docs)
    vector_store = Chroma.from_documents(docs, embedding=OpenAIEmbeddings())
    retriever = vector_store.as_retriever()
    return retriever

def getRelevantDocs(query: str):
    retriever = loadData()
    relevant_docs = retriever.invoke(query)
    return relevant_docs

def supervisorAgent(query: str, llm: ChatOpenAI, webContext, relevantDocuments):
    prompt_template = """
    Você é um gerente de uma agência de viagens. Sua resposta final deverá ser um roteiro de viagem completo e detalhado. 
    Utilize o contexto de eventos e preços de passagens, o input do usuário e também os documentos relevantes para elaborar o roteiro.
    Contexto: {webContext}
    Documento relevante: {relevant_documents}
    Usuário: {query}
    Assistente:
    """

    prompt = PromptTemplate(
        input_variables=["webContext", "relevant_documents", "query"],
        template=prompt_template,
    )

    sequence = RunnableSequence(prompt | llm)

    return sequence.invoke({"webContext": webContext, "relevant_documents": relevantDocuments, "query": query})

def getResponse(query: str, llm):
    webContext = researchAgent(query, llm)
    relevantDocuments = getRelevantDocs(query)
    response = supervisorAgent(query, llm, webContext, relevantDocuments)
    return response

def lambda_handler(event, context):
  # query = event.get("question")
  body = json.loads(event.get('body', {}))
  query = body.get('question', 'Parametro question não fornecido')
  response = getResponse(query, llm).content
  return {
    "statusCode": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": json.dumps({
      "message": "Tarefa concluída com sucesso",
      "details": response
    }), 
  }

# lambda_handler({ "question": "faca uma viagem para o brasil"}, {})
