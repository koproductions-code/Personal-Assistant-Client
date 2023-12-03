from server.Server import LLMServer

class Client:

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
