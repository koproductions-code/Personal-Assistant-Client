import json
import os
from functions.functions import *
from functions.home_assistant import *

def generate_system_prompt():
    system_prompt = "SYSTEM: You are an helpful assistant whose name is Jarvis. You have access to the following functions to help the user, you can use the functions if needed-"
    return system_prompt

def generate_functions(config_path):
    fullPath = os.path.join(config_path, "functions.json")

    if not(os.path.exists(fullPath)):
        return []

    with open(fullPath, "r") as file:
        try:
            jsonfile = json.load(file)
            return list(jsonfile["functions"])
        except Exception:
            return []

def generate_user_prompt(content):
    prompt = f"USER: {content}"
    return prompt

def generate_function_response(llm_call):
    pass

def call_function(response: str):
    try:
        response = response.replace("\n", "")
        response = response.replace("'", "")

        json_part = response.split(' ', 1)[1]

        parsed = json.loads(json_part)

    except ValueError as ve:
        print(f"Value error occurred: {ve}")
    else:
        try:
            function_name = parsed.get("name")
            if not function_name:
                raise ValueError("Function name is missing")

            arguments = parsed["arguments"]

        except ValueError as ve:
            print(f"Value error occurred: {ve}")
        else:
            try:
                if function_name in globals():
                    if len(arguments) > 0:
                        result : FunctionResponse = globals()[function_name](**arguments)
                    else:
                        result : FunctionResponse = globals()[function_name]()
                    print(result)
                    return result
                else:
                    raise NameError(f"Function {function_name} not found.")
            except TypeError as te:
                print(f"TypeError occurred: {te}")
            except NameError as ne:
                print(ne)