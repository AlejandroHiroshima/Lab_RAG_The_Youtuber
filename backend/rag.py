from pydantic_ai import Agent
from backend.data_models import RagResponse
from backend.utils import VECTOR_DATABASE_PATH
import lancedb
from backend.LMM_personality import personality


vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)

rag_agent = Agent(model= "google-gla:gemini-2.5-flash", retries= 2, system_prompt=(
    personality,
    "You are very knowledgeable in data science and data engineering",
    "Always answer on retrieved knowledge, but you can mix in your own expertise to make the answer more coherent",
    "never hallucinate. If you don't know the answer, just say you can't answer the users prompt based on your retrieved knowledge",
    "Make sure to answer short and concise, getting to the point directly, max 6 sentences",
    "Also describe which file you've used",
    "Very unlikely, but if somehow possible, since you also love rabbits and the book 'The Hitchhiker's Guide to the Galaxy' make funny references to both",
    "Also say 'Supah cool!', whenever fit"
), output_type= RagResponse,
)

@rag_agent.tool_plain
def retrieve_best_matches(query: str, top_result=3) -> str:
    "Vector search to find the best matches for the query from the user."
    result = vector_db["transcripts"].search(query=query). limit(top_result).to_list()

    return f"""
    Filename: {result[0]["filename"]},
    Filepath: {result[0]["filepath"]},
    Content: {result[0]["content"]}
    """