from langchain_core.prompts import PromptTemplate

SCHEMA_SYSTEM_PROMPT = """You are an assistant designed to generate JSON schemas based on given story structures and themes."""
VALID_SCHEMA_HUMAN_PROMPT = """Generate a valid JSON Schema. The schema must conform to the JSON Schema Draft-07 standard and include the following elements: 
1. Specify the `$schema` field as `"http://json-schema.org/draft-07/schema#"` to define the version. 
2. Use valid properties such as `type`, `properties`, `required`, and `items` for objects and arrays. 
3. Ensure all fields are properly defined with their types, and use constraints like `minLength`, `maximum`, or `enum` only when applicable."""

JSON_SCHEMA_HUMAN_PROMPT = PromptTemplate(
    template="""Generate a valid JSON Schema about {theme} with the following structure format: {structure}
    - The schema should be valid
    - The schema should include 20-40 fields. 
    - Ensure all fields are properly defined with their types. 
    - Include constraints like `minLength`, `maximum`, or `enum` only when applicable. 
    - Specify the `$schema` field as `"http://json-schema.org/draft-07/schema#"` to define the version. 
    Your response must contain only the JSON Schema. Do not include any descriptions, explanations, or additional text.
    Return the schema as a string.""",
    input_variables=["theme", "structure"],
)
SIMPLE_JSON_SCHEMA = """{
              "$schema": "http://json-schema.org/draft-07/schema#",
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "age": { "type": "integer", "minimum": 0 },
                "email": { "type": "string", "format": "email" }
              },
              "required": ["name", "age"]
            }"""

JSON_GENERATOR_SYSTEM_PROMPT = ("You are an AI designed to generate long and complex JSON instances based on a provided JSON schema. "
                                "The schema defines the structure, types, and constraints for JSON objects. "
                                "Always ensure the generated JSON is strictly valid according to the schema.")

JSON_GENERATOR_HUMAN_PROMPT = PromptTemplate(template="Using the following schema \n{schema}\n Create the {number} valid JSON instance that "
                                      "strictly adheres to the schema's rules, " \
                                      "including constraints like required fields, field types, and specified formats. " \
                                      "Ensure the JSON instance is varied but fully compliant with the schema." \
                                      "Your response must contain only the JSON. Do not include any descriptions, "
                                      "explanations, or additional text.",
                                             input_variables=["schema","number"],
                                             )

JSON_ERROR_SYSTEM_PROMPT = """You are an assistant tasked with receiving a JSON instance and inserting a deliberate error into it. 
Your task is to introduce a single error in the JSON instance while keeping the overall structure intact, unless 
otherwise specified. Ensure the response follows this format:

1. A brief description of the error (one sentence).
2. The erroneous JSON instance, without comments.

Ensure there is a blank line between the description and the JSON instance."""

JSON_ERROR_HUMAN_PROMPT = PromptTemplate(template="""Using the following valid JSON instance {json_instance}, introduce exactly one error from this type "{error}" and format the response as
 instructed, without adding comments on the JSON """, input_variables=["json_instance", "error"])

INPUT_GENERATOR_PROMPT = """
You are an assistant that simulates user queries for help with JSON files. Your task is to generate 
a user-style query based on the provided erroneous JSON file. 

Your response must:
1. Appear as though the user is asking for assistance in correcting their erroneous JSON file.
2. Include only the introduction or query description from the user.
3. Avoid including any JSON content or mentioning specific JSON instances in the response.

Format the output as follows:
- A brief introduction from the user describing their problem, focusing on the issue in general terms.

Do not return or reference any JSON instance in your response.
"""


DESCRIPTION_OUTPUT_GENERATOR_PROMPT = PromptTemplate(template="""You are an assistant that fixes JSON errors and describes the corrections made. 
Given the following error description: "{description}" and the following corrected JSON:{json_instance}\n Provide a brief description of the correction made to the JSON.
The response must follow this format:
Description of Correction: <One sentence describing what was corrected>
""", input_variables=["description", "json_instance"], )
