import os
import json

class LLMModel:
    def generate_prompt(self):
        # Implementation for generating a prompt
        raise NotImplementedError("This method should be implemented by subclasses")

    def generate_system(self):
        # Implementation for generating a system
        raise NotImplementedError("This method should be implemented by subclasses")

    def generate_functions(self, config_path):
        fullPath = os.path.join(config_path, "functions.json")

        if not(os.path.exists(fullPath)):
            return []

        with open(fullPath, "r") as file:
            try:
                jsonfile = json.load(file)
                return list(jsonfile["functions"])
            except Exception:
                return []