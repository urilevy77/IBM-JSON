from huggingface_hub import InferenceClient

from config import MODEL
from prompts import SCHEMA_SYSTEM_PROMPT, VALID_SCHEMA_PROMPT, JSON_SCHEMA_PROMPT

client = InferenceClient()
story_structure="Flat Layout: A simple list of attributes with no nesting or hierarchies."
story_theme="Nature"

chat_input = [
    {
        "role": "system",
        "content": SCHEMA_SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": f"{VALID_SCHEMA_PROMPT}"
    },
    {
        "role": "assistant",
        "content": """{
          "$schema": "http://json-schema.org/draft-07/schema#",
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "age": { "type": "integer", "minimum": 0 },
            "email": { "type": "string", "format": "email" }
          },
          "required": ["name", "age"]
        }"""
    },
    {
        "role": "user",
        "content": f"{story_structure}  {JSON_SCHEMA_PROMPT} {story_theme}"
    }
]

# Call the chat completion API
second_response = client.chat_completion(
    messages=chat_input,
    model=MODEL,
    temperature=0.8,
    max_tokens=500,
    seed=42,
)

# Extract and print the assistant's reply
schema_str = second_response.get("choices", [{}])[0].get("message", {}).get("content", "")
print(schema_str)