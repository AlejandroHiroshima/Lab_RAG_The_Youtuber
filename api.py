from fastapi import FastAPI
from backend.rag import ChatBot
from backend.data_models import Prompt
from backend.utils import VECTOR_DATABASE_PATH
import lancedb

app = FastAPI()
chatbot = ChatBot()
vector_db= lancedb.connect(uri = str(VECTOR_DATABASE_PATH))

@app.post("/rag/query")
async def query_documentation(query: Prompt):
    result = await chatbot.run(query.prompt)

    return result["bot"]

@app.get("/rag/history")
async def get_history():
    return chatbot.get_history()

@app.get("/rag/videos")
async def list_videos():
    table = vector_db['transcripts']
    df = table.to_pandas()
    filenames = df['filename'].to_list()
    return {"videos": filenames}