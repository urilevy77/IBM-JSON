SYSTEM_PROMPT = """ "story" can be defined as a structured representation of information that outlines a specific
      theme or subject matter. each "story" consists set of attributes that provide detailed data points related to that theme.
       The attributes serve to describe various aspects of the story, allowing for a comprehensive understanding of the subject.
     """
SCHEMA_SYSTEM_PROMPT = """You are an assistant designed to generate JSON schemas based on given story structures and
                       themes."""
VALID_SCHEMA_PROMPT = """Generate a valid JSON Schema using the above Structure format and the following theme. 
The schema must conform to the JSON Schema Draft-07 standard and include the following elements:

1. Specify the `$schema` field as `"http://json-schema.org/draft-07/schema#"` to define the version. 2. Use valid 
properties such as `type`, `properties`, `required`, and `items` for objects and arrays. 3. Ensure all fields are 
properly defined with their types, and use constraints like `minLength`, `maximum`, or `enum` only when applicable. """

JSON_SCHEMA_PROMPT = """ Generate a valid JSON Schema using the above Structure format and the following theme. 
The schema should be valid and vary in size based on the specified size category:

- **Small Schema**: Includes 3-5 fields.
- **Medium Schema**: Includes 6-10 fields.
- **Large Schema**: Includes 11-15 fields.

Your response must contain only the JSON Schema. Do not include any descriptions, explanations, or additional text.
Choose the size randomly, without mentioning which one you chose."""
JSON_GENERATOR_SYSTEM_PROMPT = ("You are an AI designed to generate JSON instances based on a provided JSON schema. "
                                "The schema defines the structure, types, and constraints for JSON objects.")
JSON_PROMPT = " Using the above schema, create a valid " \
              "JSON instance that follow the rules specified. Ensure the JSON instance is diverse and cover " \
              "different variations allowed by the schema. " \
              "Your response must contain only the JSON. Do not include any descriptions, explanations, " \
              "or additional text." \
              "Choose the size randomly, without mentioning which one you chose."
JSON_ERROR_SYSTEM_PROMPT = ("You are an AI designed to create invalid JSON instances based on a provided JSON schema. "
                            "Your task is to introduce exactly one error in the JSON instance. The error can be "
                            "related to missing required fields, incorrect data types, or violating constraints.")
JSON_ERROR_PROMPT = """Using the following valid JSON instance, introduce exactly one error: """
