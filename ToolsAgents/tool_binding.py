from tool_creation import multiply
from langchain_openai import ChatOpenAI
import dotenv
dotenv.load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)

# Bind tools to llm
llm_with_tool = llm.bind_tools(tools=[multiply])
print(llm_with_tool)

# Run the llm with tool
result = llm_with_tool.invoke(
    "what is 3 times 4?"
)

print(result)




