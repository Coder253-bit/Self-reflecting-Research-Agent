from agent import LLM_Model
from openai import OpenAI


class Tools:
    def __init__(self):
        self.client = OpenAI()

        
    def research_tool(self, topic: str) -> str:
        """Researches a topic using web search and returns a summary with a URL"""
        response = self.client.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search"}],
        input=f"Give me the latest information about {topic}. Include a title, summary in 2 short sentences and a source URL. Ensure the information does not exceed 70 words incuding title, summary and URL."
        )
        # returning a string of research
        return response.output_text   