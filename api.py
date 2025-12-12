from fastapi import FastAPI, HTTPException
from backend.rag import ChatBot, DescriptionAgent, TagsAgent
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
    result = await chatbot.chat(query.prompt)
    return result["bot"]

@app.get("/rag/history")
async def get_history():
    return chatbot.get_history()

@app.get("/rag/videos")
async def list_videos():
    df = get_df()
    filenames = df['filename'].to_list()
    return {"videos": filenames}

#below function is partly LLM generated
@app.get("/rag/videos/{filename}/description")
async def make_description(filename: str):
    df= get_df()
    match = df[df['filename'] == filename]
    if match.empty:
        raise HTTPException(status_code=404, detail=f" Video/Transcript '{filename}' don't exist in database")
    content = match.iloc[0]['content']
    instruction = f"""
    Summarize this transcript:
    {content}
    """
    result = await desc_bot.run(instruction)
    return Description(
        doc_id = filename,
        description = result
    )

@app.get("/rag/videos/{filename}/tags")
async def make_tags(filename: str):
    df = get_df()
    match= df[df['filename']== filename]
    if match.empty:
        raise HTTPException(status_code=404, detail=f" Video/Transcript '{filename}' don't exist in database")
    content = match.iloc[0]['content']
    instruction = f"""
    Create singleword, comma-separated Youtube tags from this transcript,
    return only the tags, no extra text, no numbering etc.
    Transcript:
    {content}
    """
    result= await tag_agent.create_tags(instruction)
    return Tags(
        doc_id= filename,
        tags= result
    )