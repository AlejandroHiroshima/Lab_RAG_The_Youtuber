from fastapi import FastAPI, HTTPException
from backend.rag import ChatBot
from backend.data_models import Prompt, Description
from backend.utils import VECTOR_DATABASE_PATH
import lancedb

app = FastAPI()
chatbot = ChatBot()
vector_db= lancedb.connect(uri = str(VECTOR_DATABASE_PATH))
table = vector_db['transcripts']
df = table.to_pandas()

@app.post("/rag/query")
async def query_documentation(query: Prompt):
    result = await chatbot.run(query.prompt)
    return result["bot"]

@app.get("/rag/history")
async def get_history():
    return chatbot.get_history()

@app.get("/rag/videos")
async def list_videos():
    filenames = df['filename'].to_list()
    return {"videos": filenames}

#below function is partly LLM generated
@app.get("/rag/videos/{filename}/description")
async def make_description(filename: str):
    match = df[df['transcripts'] == filename]
    if match.empty:
        raise HTTPException(status_code=404, detail=f" Video/Transcript '{filename}' don't exist in database")
    content = match.iloc[0]['content']
    instruction = f"""
    Write a short yet informative description of this Youtube transcript. Maximum 6 sentences. Don't hallucinate.
    Transcript:
    {content}
    """
    result = await chatbot.run(instruction)
    return Description(doc_id=filename, description= result)

@app.get("/rag/videos/{filename}/tags")