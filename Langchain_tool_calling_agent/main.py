from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
import os
from langchain.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from tools import search_tool, wiki_tool, save_txt_tool

load_dotenv()

# Define the schema for the structured output
class ResponseStructure(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Define the parser for the structured output
parser = PydanticOutputParser(pydantic_object=ResponseStructure)

# Define the chat template
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a research assistant that will generate a short research paper.
         Answer the user query and use necessary sources and tools.
         Wrap the response in this structured format and no other text \n {format_instruction}.
         """),
        ("placeholder", "{chat_history}"),
        ("human", "{user_query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instruction = parser.get_format_instructions())


# Create a ChatOpenAI model (OpenAI GPT-4o-mini)
llm_model_openai = ChatOpenAI(model="gpt-4o-mini")

# Setup open source LLM (Gemma-3 with HuggingFace)
HF_TOKEN=os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID="google/gemma-3-27b-it"

# Load the open source LLM
open_llm_model = HuggingFaceEndpoint(
    repo_id=HUGGINGFACE_REPO_ID,
    temperature=0.5,
    model_kwargs={"token":HF_TOKEN,
                  "max_length":"512"}
)
chat_model_llm =  ChatHuggingFace(llm = open_llm_model)


# Create the agent
agent = create_tool_calling_agent(
    llm=llm_model_openai, 
    tools=[search_tool,wiki_tool,save_txt_tool], 
    prompt=prompt_template
    )

# Create the executor
agent_executor = AgentExecutor(agent=agent, tools=[search_tool,wiki_tool,save_txt_tool], verbose=True)


# take user input
user_query = input("Write Query Here: ")
# Invoke the agent
# raw_response = agent_executor.invoke({"user_query": "tell me about very deep sea creatures?"})
raw_response = agent_executor.invoke({"user_query": user_query})
print(raw_response)

# structured output
try:
    structured_output = parser.parse(raw_response.get("output"))
    print(f"Structured Output Topic: {structured_output.topic}")
except Exception as e:
    print(f"Failed to parse structured output. Error: {e} \n Output: {structured_output}")


