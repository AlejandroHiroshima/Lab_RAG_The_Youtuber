from fastapi import FastAPI
from backend.rag import ChatBot
from backend.data_models import Prompt

app = FastAPI()
chatbot = ChatBot()

@app.post("/rag/query")
async def query_documentation(query: Prompt):
    result = await chatbot.run(query.prompt)

    return result["bot"]

@app.get("/rag/history")
async def get_history():
    return chatbot.get_history()

@app.get("/rag/get_videos")
async def get_videos()
    pass