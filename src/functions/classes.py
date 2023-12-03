class FunctionResponse(object):
    def __init__(self, return_to_assistant, result) -> None:
        self.return_to_assistant = return_to_assistant
        self.result = result