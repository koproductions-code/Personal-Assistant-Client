import requests

class LLMServer:

    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port

    def request(self, system, functions, prompt):
        body = {}

        body["system"] = system
        body["functions"] = str(functions)
        body["prompt"] = prompt

        result = requests.post(f"http://{self.host}:{self.port}/request", json=body)

        try:
            result = result.json()["response"]
            return result
        except Exception as e:
            print(result.json())
            raise e