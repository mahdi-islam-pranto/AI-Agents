from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import os

# Define the tool DuckDuckGo
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search_tool", func=search.run, description="Searches the web for information"
    )

# define the wikipedia tool
wiki_api = WikipediaAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=200
)
wiki_tool = WikipediaQueryRun(api_wrapper= wiki_api)


# define a custom tool
def save_to_local_file(data:str, file_name:str = "ai_response.txt"):
    timeStamps = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_data = f"----Output----- \n Time: {timeStamps}\n\n{data}"
    get_current_directory_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(get_current_directory_path, file_name)
    
    with open(file_name, "a", encoding='utf-8') as file:
        file.write(formatted_data)
    return "Data saved to local file successfully"

save_txt_tool = Tool(
    name="save_txt_tool",
    func=save_to_local_file,
    description="Saves the output to a local file"
)

