# Synthetic Data Generation

## Overview
This project generates synthetic JSON data, introduces errors into the data, and validates the errors to create structured training data for large language models (LLMs). The workflow includes:

1. Generating JSON schemas based on predefined story structures and themes.
2. Creating valid JSON instances from the schemas.
3. Introducing controlled errors into the JSON instances.
4. Validating the erroneous JSON instances.
5. Generating user-like queries and model responses for training purposes.

The generated dataset is useful for training models to detect and correct JSON-related errors.

---

## Features
✅ Generates structured JSON schemas dynamically based on themes and structures.
✅ Produces valid JSON instances from schemas.
✅ Introduces controlled errors in JSON data.
✅ Validates JSON instances against schemas.
✅ Simulates user queries for JSON correction.
✅ Provides structured input-output pairs for training LLMs.

---

## Installation

Ensure you have Python installed, then install the required dependencies:

```sh
pip install -r requirements.txt
```

---

## Usage
Run the main script with the following arguments:

```sh
python main.py <num_of_jsons> <story_structure_path> <theme_path> <errors_path> <input_log_path> <output_log_path>
```

- `<num_of_jsons>`: Number of JSON instances to generate per schema.
- `<story_structure_path>`: Path to the file containing story structures.
- `<theme_path>`: Path to the file containing story themes.
- `<errors_path>`: Path to the file containing error types.
- `<input_log_path>`: Path to save user-generated inputs.
- `<output_log_path>`: Path to save model-generated outputs.

Example:

```sh
python main.py 5 story_structures.txt themes.txt errors.txt input_log.txt output_log.txt
```

---

## Project Structure

```
├── main.py             # Entry point, controls data generation flow
├── generators.py       # Generates JSON schemas, instances, and errors
├── validation.py       # Validates JSON schemas and instances
├── data_store.py       # Stores and manages JSON error datasets
├── prompts.yaml        # Stores model prompts for text generation
├── requirements.txt    # Dependencies
```

---

## How It Works

1. **Load Inputs**: Reads story structures, themes, and error types.
2. **Generate JSON Schema**: Uses an LLM to create a structured JSON schema.
3. **Generate JSON Instances**: Produces valid JSON data from schemas.
4. **Introduce Errors**: Modifies valid JSONs to introduce controlled mistakes.
5. **Validate JSONs**: Ensures errors cause schema violations.
6. **Generate Training Data**: Simulates user queries and model corrections.

---

## Dependencies
- `langchain`
- `python-dotenv`
- `huggingface-hub`
- `jsonschema`
- `inflect`
- `pyyaml`
- `sentencepiece`

Install them using:

```sh
pip install -r requirements.txt
```

