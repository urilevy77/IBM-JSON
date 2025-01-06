import random
from typing import ClassVar

import inflect
from langchain.chains.base import Chain
from generators import json_schema_generator, json_generator, error_generator, input_generator, \
    description_output_generator
from langchain.chains import SequentialChain

from utils import insert_schemas_to_arr
from validation import json_schema_validator, json_validator


class JSONSchemaGeneratorChain(Chain):
    input_keys: ClassVar = ["story_structure", "story_theme"]
    output_keys: ClassVar = ["schema_str"]

    def _call(self, inputs):
        schema_str = json_schema_generator(inputs["story_structure"], inputs["story_theme"])
        if json_schema_validator(schema_str):
            # insert_schemas_to_arr(schema_str)

            return {"schema_str": schema_str}


class JSONGeneratorChain(Chain):
    input_keys: ClassVar = ["schema_str", "json_num"]
    output_keys: ClassVar = ["json_instances"]

    def _call(self, inputs):
        json_instances = []
        num_to_string = inflect.engine()
        for i in range(inputs["json_num"]):
            json_file = json_generator(inputs["schema_str"], num_to_string.ordinal(i + 1))

            if json_validator(json_file, inputs["schema_str"]):
                json_instances.append(json_file)

        # insert_json_arr_to_arr(json_instances)

        return {"json_instances": json_instances}


class ErrorGeneratorChain(Chain):
    input_keys: ClassVar = ["json_instances", "error_file", "schema_str"]
    output_keys: ClassVar = ["array_with_all_data"]

    def _call(self, inputs):
        arr_with_all_data = []
        for json_instance in inputs["json_instances"]:
            with open(inputs["error_file"], 'r') as error_file:
                if json_instance is not None:
                    for error_type in error_file:
                        json_with_error, description = error_generator(json_instance, error_type)
                        if description and json_with_error:
                            arr_with_all_data.append(
                                {"json with error": json_with_error, "schema": inputs["schema_str"],
                                 "json instance": json_instance,
                                 "error description": description})
                            print("Description: ", description)
                            print("Json: ", json_instance)
                            print("Json error: ", json_with_error)
        return {"array_with_all_data": arr_with_all_data}


class InputOutputGeneratorChain(Chain):
    input_keys: ClassVar = ["array_with_all_data"]
    output_keys: ClassVar = ["arr_of_input_output_dicts"]

    def _call(self, inputs):
        # Use the input_generator function
        arr_of_input_output_dicts = []
        for data in inputs["array_with_all_data"]:
            user_input = input_generator(data["json with error"])
            model_output = description_output_generator(data['error description'], data["json instance"])
            model_output_with_json = f'{model_output}\n```json\n{data["json instance"]}\n```'
            with_json_initial = random.randint(0, 1)
            if data['json with error'].startswith("```") or with_json_initial == 0:
                user_input_with_json_error = f"{user_input}\n{data['json with error']}"
            else:
                user_input_with_json_error = f"{user_input}\n```json\n{data['json with error']}\n```"
            arr_of_input_output_dicts.append({"user input": user_input_with_json_error,
                                              "model output": model_output_with_json})

        print(arr_of_input_output_dicts)
        return {"arr_of_input_output_dicts": arr_of_input_output_dicts}


# Define individual chains
schema_chain = JSONSchemaGeneratorChain()
json_chain = JSONGeneratorChain()
error_chain = ErrorGeneratorChain()
input_output_chain = InputOutputGeneratorChain()

# Combine chains into a pipeline
pipeline = SequentialChain(
    chains=[schema_chain, json_chain, error_chain, input_output_chain],
    input_variables=["story_structure", "story_theme", "json_num", "error_file"],
    output_variables=["arr_of_input_output_dicts"]
)
