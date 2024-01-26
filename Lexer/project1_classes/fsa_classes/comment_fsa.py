from .fsa import FSA
from typing import Callable as function

class COMMENT_FSA(FSA):
    def __init__(self):
        FSA.__init__(self, "COMMENT")
        self.accept_states.add(self.s2)
        self.token_name = "COMMENT"

    def s0(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        # Check if the input starts with a hash character (#)
        if current_input == '#':
            next_state = self.s1
            self.value += current_input
        else:
            next_state = self.s_err 

        return next_state

    def s1(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        # Consume input until the end of the line or end of the file
        if current_input != '\n':
            next_state = self.s1
            self.value += current_input
        else:
            next_state = self.s2

        return next_state

    def s2(self) -> function:
        # Reached the end of the line or end of the file
        next_state: function = self.s2
        self.num_chars_read += 1
        return next_state

    def s_err(self) -> function:
        next_state: function = self.s_err  # Stay in error state for invalid input
        self.num_chars_read += 1
        return next_state
