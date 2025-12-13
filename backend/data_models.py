from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model= get_registry().get("gemini-text").create(name="gemini-embedding-001")

class Transcript(LanceModel):
    doc_id: str = Field(description="unique identifier for the file")
    filepath: str = Field(description="path of the file")
    filename: str = Field(description="Name of the file, without the suffix")
    content: str = embedding_model.SourceField()
    embedding: Vector(embedding_model.ndims()) = embedding_model.VectorField()

class Prompt(BaseModel):
    prompt: str = Field(description="prompt from the user")

class RagResponse(BaseModel):
    filename: str = Field(description= "file name of retrieved file, without the suffix")
    filepath: str = Field(description= "absolute path to the retrieved file")
    answer: str = Field(description="answer based on the retrieved file")

class Description(BaseModel):
    doc_id: str = Field(description="unique name of the file")
    description: str = Field(description="Short description of the contents of the transcript from it's Youtube video")

class Tags(BaseModel):
    doc_id: str = Field(description="unique name of the file")
    tags: str = Field(description="20-40 comma-separated Youtube tags, example: 'keyword1, keyword2, keyword3' etc...")