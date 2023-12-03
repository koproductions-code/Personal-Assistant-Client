from models.BaseModel import LLMModel
from functions.functions import *
import os
import json

class Llama2_Model(LLMModel):
    
    def __init__(self):
        self.B_FUNC, self.E_FUNC = "<FUNCTIONS>", "</FUNCTIONS>\n\n"
        self.B_INST, self.E_INST = "[INST] ", " [/INST]"

    def generate_prompt(self, prompt):
        if prompt is None or prompt == "":
            return None
        
        return self.B_INST + prompt + self.E_INST

    def generate_system(self):
        return ""

    def generate_functions(self, config_path):
        fullPath = os.path.join(config_path, "functions.json")
        
        if not(os.path.exists(fullPath)):
            return self.B_FUNC + "[]" + self.E_FUNC

        with open(fullPath, "r") as file:
            try:
                jsonfile = json.load(file)
                return self.B_FUNC + json.dumps(jsonfile["functions"]) + self.E_FUNC
            except Exception:
                return self.B_FUNC + "[]" + self.E_FUNC
            
    def handle_response(self, response: str, myrequest: str):
        response = response.split("[/INST]")[1]

        if '"function"' in response:
            start = response.find('"function"')-2
            end = response.find('```', start+1)

            text = response[start:end]
            try: 
                myjson = json.loads(text)
                print(f"Calling function: {myjson}")
                self.call_function(myjson)
            except Exception as e:
                print(e)
                print(text)
        else:
            print("Error2")
            print(response)

    def call_function(self, parsed: dict):
        try:
            function_name = parsed.get("function")
            if not function_name:
                raise ValueError("Function name is missing")

            arguments = parsed["arguments"]

        except ValueError as ve:
            print(f"Value error occurred: {ve}")
        else:
            try:
                if function_name in globals():
                    result : FunctionResponse = globals()[function_name](**arguments)
                    return result
                else:
                    raise NameError(f"Function {function_name} not found.")
            except TypeError as te:
                print(f"TypeError occurred: {te}")
            except NameError as ne:
                print(ne)