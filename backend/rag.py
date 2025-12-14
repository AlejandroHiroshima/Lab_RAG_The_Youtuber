from pydantic_ai import Agent
from backend.data_models import RagResponse, Tags, Description
from backend.utils import VECTOR_DATABASE_PATH
import lancedb
from pathlib import Path

PERSONALITY_FILE = Path(__file__).parents[1] / "assets/personality.txt"
with open(PERSONALITY_FILE, "r", encoding="utf-8") as file:
    personality_LMM_analysis = file.read()

vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)

class ChatBot:
    def __init__(self):
        self.chat_agent = Agent(model= "google-gla:gemini-2.5-flash", retries= 2, system_prompt=(
        personality_LMM_analysis,
        "You are very knowledgeable in data science and data engineering",
        "Always answer on retrieved knowledge, but you can mix in your own expertise to make the answer more coherent",
        "never hallucinate. If you don't know the answer, just say you can't answer the users prompt based on your retrieved knowledge",
        "Make sure to answer short and concise, getting to the point directly, max 6 sentences",
        "Also describe which file you've used",
        "Very unlikely, but if somehow possible, since you also love rabbits and the book 'The Hitchhiker's Guide to the Galaxy' make funny references to both",
        "Also say 'Supah cool!', whenever fit"
        ), output_type= RagResponse,
        )
        self.history = []
     
        self._register_tools()
    def _register_tools(self):
        @self.chat_agent.tool_plain
        def retrieve_best_matches(query: str, top_result=3) -> str:
            "Vector search to find the best matches for the query from the user."
            result = vector_db["transcripts"].search(query=query).limit(top_result).to_list()
            
            context = "\n\n".join([
                f"Filename: {doc['filename']}\nFilepath: {doc['filepath']}\nContent: {doc['content']}"
                for doc in result
            ])
            return context
        # part below function much thank to LLM
    async def chat(self, prompt: str) -> RagResponse:
        message_history= self.history if self.history else None
        self.result = await self.chat_agent.run(prompt, message_history=message_history)

        rag_response: RagResponse = self.result.output
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": rag_response.answer})
        return rag_response
    
    def get_history(self)-> list[dict]:
        return self.history

class DescriptionAgent():
    def __init__(self):
        self.desc_agent = Agent(
            model="google-gla:gemini-2.5-flash", 
            retries=2, 
            system_prompt="You make short and engaging summaries of youtube transcripts. Maximum 6 sentences, no hallucinations",
            output_type= Description)
        
    async def run(self, filename: str, content: str) -> Description:
        instruction = f"""
        Summarize this transcript:
        {content}
        """
        self.result = await self.desc_agent.run(instruction)
        return self.result.output

class TagsAgent():
    def __init__(self):
        self.tag_agent = Agent(
           model="google-gla:gemini-2.5-flash", 
            retries=2, 
            system_prompt=("From the transcript given to you, summarize to 20-40 tags for Youtube",
                           "Return only a comma-separated list of keywords",
                           "example format: data engineering, python, ELT, terraform, sql"),
            output_type= Tags) 
        
    async def create_tags(self, filename: str, content: str) -> Tags:
        instruction = f"""
        Create singleword, comma-separated Youtube tags from this transcript,
        return only the tags, no extra text, no numbering etc.
        Transcript:
        {content}
        """
        self.result = await self.tag_agent.run(instruction)
        return self.result.output