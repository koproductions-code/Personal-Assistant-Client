from server.Server import LLMServer
from datetime import datetime

"""
TODO:
Function Returns
Generalize Call Function 
"""

class CLIClient:

    def __init__(self, host, port, config, model) -> None:
        self.server = LLMServer(str(host), str(port))
        self.config = config
        self.model = model

    def request(self, prompt):
        system = self.model.generate_system()
        functions = self.model.generate_functions(self.config)
        prompt = self.model.generate_prompt(prompt)

        result = self.server.request(system, functions, prompt)
        self.model.handle_response(result, prompt)
    
    def main(self):
        while True:
            prompt = input("Prompt: ")
            start_time = datetime.now()
            self.request(prompt)
            end_time = datetime.now()

            time_difference = end_time - start_time
            print(f"Time: {time_difference.total_seconds()}")