from typing import Any
from .my_token import Token

class Parameter():
    def __init__(self, name: str, parameters: list[str]):
        self.name = name
        self.parameters = parameters

    def to_string(self):
        param_str: str = ""
        param_str = ','.join(self.parameters)
        return f'{self.name}({param_str}).'
    
    def is_constant(self) -> bool:
        return all("'" in param for param in self.parameters)