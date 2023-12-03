from models.BaseModel import LLMModel
from functions.utils import call_function

class GlaiveAI_Model(LLMModel):
    
    def __init__(self):
        pass

    def generate_prompt(self, prompt):
        if prompt is None or prompt == "":
            return None
        
        return f"USER: {prompt}"
    
    def generate_system(self):
        return "SYSTEM: You are an helpful assistant whose name is Jarvis. You have access to the following functions to help the user, you can use the functions if needed-" 
    
    def handle_response(self, response: str, myrequest: str):
        if "<functioncall>" in response:
            split = response.split("<functioncall>")[1]
            newprompt = "<functioncall>" + split
            print("Calling function: {}".format(newprompt))
            _ = call_function(newprompt)
        elif "ASSISTANT: " in response:
            split = response.split("ASSISTANT: ")[1]
            print(split)
        else:
            print("There was an error.")
            print(response)