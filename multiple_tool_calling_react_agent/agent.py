from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from dotenv import load_dotenv
load_dotenv()

# make tools

# web search tool
@tool
def search(query: str) -> str:
    """Searches the web for the query."""
    search = DuckDuckGoSearchRun()
    return search.run(query)

# weather tool
@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=fc2732c6b5257127c0aefbe5cf7ed68a&query={city}'
  
  response = requests.get(url)
  data = response.json()
  if "current" not in data:
    return "Weather data is not avaiable"
  current = data["current"]
  location = data.get("location", {})
  air_quality = current.get("air_quality", {})
  summary = (
        f"Weather in {location.get('name', city)}, {location.get('country', '')}:\n"
        f"- Temperature: {current.get('temperature', 'N/A')}°C\n"
        f"- Weather: {', '.join(current.get('weather_descriptions', []))}\n"
        f"- Wind: {current.get('wind_speed', 'N/A')} km/h from {current.get('wind_dir', 'N/A')}\n"
        f"- Humidity: {current.get('humidity', 'N/A')}%\n"
        f"- Cloud Cover: {current.get('cloudcover', 'N/A')}%\n"
        f"- Feels Like: {current.get('feelslike', 'N/A')}°C\n"
        f"- UV Index: {current.get('uv_index', 'N/A')}\n"
        f"- Visibility: {current.get('visibility', 'N/A')} km\n"
        f"- Air Quality (US EPA Index): {air_quality.get('us-epa-index', 'N/A')}\n"
    )
  return summary

# ai doctor tool
@tool
def get_ai_doctor(query: str) -> str:
   """
   This function calls the llm (doctor llm) to get the medical answer for the query
   """
   llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
   response = llm.invoke(query)
   return response

# ai math teacher tool
@tool
def get_ai_math_teacher(query: str) -> str:
   """
   This function calls the llm (math llm) to get the math answer for the query
   """
   llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
   response = llm.invoke(query)
   return response

# ai history teacher tool
@tool
def get_ai_history_teacher(query: str) -> str:
   """
   This function calls the llm (history llm) to get the historical answer for the query
   """
   llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
   response = llm.invoke(query)
   return response


# get a prebuild react agent prompt from lanchain hub
react_prompt = hub.pull("hwchase17/react")
# define agent
agent = create_react_agent(
   llm=ChatOpenAI(model="gpt-4o", temperature=0.2),
   tools=[search, get_weather_data, get_ai_doctor, get_ai_math_teacher, get_ai_history_teacher],
   
   prompt=react_prompt,
   )


# make the and Wrap it with AgentExecutor
agent_executor = AgentExecutor(
   agent=agent,
   tools=[search, get_weather_data, get_ai_doctor, get_ai_math_teacher, get_ai_history_teacher],
   verbose=True,
)

# run the agent
result = agent_executor.invoke({"input": "What is the weather in New York?"})
print(result)
