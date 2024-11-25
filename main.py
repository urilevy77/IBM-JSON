from huggingface_hub import InferenceClient

SYSTEM_PROMPT = """ "story" can be defined as a structured representation of information that outlines a specific
      theme or subject matter. each "story" consists set of attributes that provide detailed data points related to that theme.
       The attributes serve to describe various aspects of the story, allowing for a comprehensive understanding of the subject.
     """
JSON_SCHEMA_PROMPT = """ Generate JSON Schema using the above Structure format and the following theme: """
JSON_PROMPT = "You are an AI designed to generate JSON instances based on a provided JSON schema. The schema defines " \
                  "the structure, types, and constraints for JSON objects. Using the following schema, create valid " \
                  "JSON instances that follow the rules specified. Ensure the JSON instances are diverse and cover " \
                  "different variations allowed by the schema. "
JSON_ERROR_PROMPT = """You are an AI designed to create a single invalid JSON example based on a provided JSON 
    schema. Your task is to introduce exactly one error in the JSON instance. This error can be related to: 
    A missing required field.
    use the following JSON: """
MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def json_schema_generator(file_path, theme_path):
    with open(file_path, 'r') as file:
        for line in file:
            structure = line.strip()
            with open(theme_path, 'r') as theme_file:
                for item in theme_file:
                    theme = item.strip()
                    second_response = client.text_generation(
                        prompt=structure + JSON_SCHEMA_PROMPT + theme,
                        model=MODEL,
                        temperature=0.8,
                        max_new_tokens=500,
                        seed=42,
                        return_full_text=False,
                    )
                    print(second_response)


def json_generator(schema_path):
    with open(schema_path, 'r') as file:
        content = file.read()
        response = client.text_generation(
            prompt= JSON_PROMPT + " " + content,
            model=MODEL,
            temperature=0.8,
            max_new_tokens=500,
            seed=44,
            return_full_text=False,
        )
        print(response)


def error_generator(json_path):
    with open(json_path, 'r') as file:
        content = file.read()
        response = client.text_generation(
            prompt=JSON_ERROR_PROMPT + " " + content,
            model=MODEL,
            temperature=0.8,
            max_new_tokens=500,
            seed=44,
            return_full_text=False,
        )
        print(response)


if __name__ == "__main__":
    client = InferenceClient()


