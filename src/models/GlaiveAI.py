from models.BaseModel import LLMModel
from functions.utils import call_function

class GlaiveAI_Model(LLMModel):
    
    def __init__(self, config):
        self.config = config

    def generate_prompt(self, prompt, user=True):
        if prompt is None or prompt == "":
            return None
        
        if user:
            prompt = "USER: " + prompt

        return prompt
    
    def generate_function_return(self, response):
        return "FUNCTION CALL: " + response.result["info"]

    def generate_system(self):
        return "SYSTEM: You are an helpful assistant whose name is Jarvis. You have access to the following functions to help the user, you can use the functions if needed-" 
    
    def handle_response(self, response: str, orig_prompt: str, server, on_response = None):
        if "<functioncall>" in response:
            split = response.split("<functioncall>")[1]
            newprompt = "<functioncall>" + split
            print("Calling function: {}".format(newprompt))
            result = call_function(newprompt)

            if result.return_to_assistant == True:
                function_return = self.generate_function_return(result)
                history = self.generate_prompt(orig_prompt, False) + "\n" + "ASSISTANT: <functioncall> {'name': 'get_calendar', 'arguments': {}}"
                new_response = server.request(self.generate_system(), self.generate_functions(self.config), history + "\n" + function_return)

                assistant_answer = new_response.split("ASSISTANT: ")
                assistant_answer = assistant_answer[len(assistant_answer)-1]
                
                if on_response != None:
                    on_response(assistant_answer)
                
                print("ASSISTANT: " + assistant_answer)
            
        elif "ASSISTANT: " in response:
            assistant_answer = response.split("ASSISTANT: ")[1]
            if on_response != None:
                    on_response(assistant_answer)

            print("ASSISTANT: " + assistant_answer)
        else:
            print("There was an error.")
            print(response)