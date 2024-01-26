from .fsa import FSA
from typing import Callable as function

class ID_FSA(FSA):
    def __init__(self):
        FSA.__init__(self, "ID")
        self.accept_states.add(self.s3)
        self.accept_states.add(self.s1)
        self.token_name = "ID"
        self.checker = ["Schemes","Rules","Queries","Facts"]

    def s0(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input.isalpha():
            next_state = self.s1
            self.value += current_input
        else:
            next_state = self.s_err

        return next_state

    def s1(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input.isalnum():
            next_state = self.s1
            self.value += current_input
        else:
            next_state = self.s3

        return next_state

    def s3(self) -> function:
        next_state: function = self.s3
        self.num_chars_read += 1
        return next_state

    def s_err(self) -> function:
        next_state: function = self.s_err  
        self.num_chars_read += 1
        return next_state
