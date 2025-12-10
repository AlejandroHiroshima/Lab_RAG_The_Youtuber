from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model= get_registry().get("gemini-text").create(name="gemini-embedding-001")

class Transcript(LanceModel):
    doc_id: str
    filepath: str
    filename: str = Field(description="Name of the file, without the suffix")
    content: str = embedding_model.SourceField()
    embedding: Vector(3072) = embedding_model.VectorField()