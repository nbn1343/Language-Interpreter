from .fsa import FSA
from typing import Callable as function

class STRING_FSA(FSA):
    def __init__(self):
        FSA.__init__(self, "String")  # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s2)
        self.token_name = "STRING"

    def s0(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == "'":
            next_state = self.s1
            self.value += "'"
        else:
            next_state = self.s_err

        return next_state
    
    def s1(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input != "'":
            next_state = self.s1
            self.value += current_input
        else:
            next_state = self.s2
            self.value += "'"

        return next_state
    
    def s2(self) -> function:
        next_state: function = self.s2 
        self.num_chars_read += 1
        return next_state
    
    def s_err(self) -> function:
        next_state = self.s_err 
        self.num_chars_read += 1
        return next_state



