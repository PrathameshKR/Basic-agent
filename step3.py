import json
from google import genai

load_dotenv()

client = genai.client()

def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

TOOL_SCHEMAS = [
    {
        "type": "function",
        
    }
]