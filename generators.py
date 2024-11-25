from prompts import JSON_SCHEMA_PROMPT, JSON_PROMPT, JSON_ERROR_PROMPT, VALID_SCHEMA_PROMPT
from schema_validation import json_schema_validator
import json

def json_schema_generator(story_structure, story_theme):
    # Chat-style input with roles
    chat_input = [
        {
            "role": "system",
            "content": "You are an assistant designed to generate JSON schemas based on given story structures and themes."
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
    generated_schema = json.loads(schema_str)
    json_schema_validator(generated_schema)


def json_generator(json_schema):
    response = client.text_generation(
        prompt=f"{JSON_PROMPT} {json_schema}",
        model=MODEL,
        temperature=0.8,
        max_new_tokens=500,
        seed=44,
        return_full_text=False,
    )
    print(response)


def error_generator(json_without_error):
    response = client.text_generation(
        prompt=f"{JSON_ERROR_PROMPT} {json_without_error}",
        model=MODEL,
        temperature=0.8,
        max_new_tokens=500,
        seed=44,
        return_full_text=False,
    )
    print(response)

