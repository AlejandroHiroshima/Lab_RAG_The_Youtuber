from google import genai
from google.genai import types
from backend.utils import THE_YOUTUBER_PIC_PATH
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = {"parts": [
        {"text": "Try describing the personality of the person in this animated picture"},
        {"inline_data": {
            "mime_type": "image/png",
            "data": open(THE_YOUTUBER_PIC_PATH, "rb").read()
        }}
    ]
    },
    config = types.GenerateContentConfig(
        temperature=0.7,
        thinking_config= types.ThinkingConfig(thinking_budget = 0))

)
personality = response.text
print(personality)