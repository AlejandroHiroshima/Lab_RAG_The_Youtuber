from fastapi import FastAPI, HTTPException
from backend.rag import ChatBot, DescriptionAgent, TagsAgent, RagResponse
from backend.data_models import Prompt, Description, Tags
from backend.utils import VECTOR_DATABASE_PATH
import lancedb

app = FastAPI()
chatbot = ChatBot()
desc_bot = DescriptionAgent()
tag_agent= TagsAgent()

vector_db= lancedb.connect(uri = str(VECTOR_DATABASE_PATH))
def get_df():
    table = vector_db['transcripts']
    df = table.to_pandas()
    return df

@app.post("/rag/query")
async def query_documentation(query: Prompt):
    result: RagResponse = await chatbot.chat(query.prompt)
    return result

# below(history) is partly due to LLM
@app.get("/rag/history")
async def get_history():
    history = chatbot.get_history()
    if not history:
        return {"message": "No history found"}
    return {"history": history}

@app.get("/rag/videos")
async def list_videos():
    df = get_df()
    filenames = df['filename'].to_list()
    return {"videos": filenames}

#below functions is partly LLM generated
@app.get("/rag/videos/{filename}/description")
async def make_description(filename: str):
    df= get_df()
    match = df[df['filename'] == filename]
    if match.empty:
        raise HTTPException(status_code=404, detail=f" Video/Transcript '{filename}' don't exist in database")
    content = match.iloc[0]['content']
    result: Description = await desc_bot.run(filename, content)
    return result

@app.get("/rag/videos/{filename}/tags")
async def make_tags(filename: str):
    df = get_df()
    match= df[df['filename']== filename]
    if match.empty:
        raise HTTPException(status_code=404, detail=f" Video/Transcript '{filename}' don't exist in database")
    content = match.iloc[0]['content']
    result: Tags = await tag_agent.create_tags(filename, content)
    return result