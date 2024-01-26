from .fsa import FSA
from typing import Callable as function

class RULES_FSA(FSA):
    def __init__(self):
        FSA.__init__(self, "Rules") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s5)
        self.token_name = "RULES"
    
    def s0(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'R':
            next_state = self.s1
            self.value += 'R'
        else:
            next_state = self.s_err

        return next_state

    def s1(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'u':
            next_state = self.s2
            self.value += 'u'
        else:
            next_state = self.s_err

        return next_state
    
    def s2(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'l':
            next_state = self.s3
            self.value += 'l'
        else:
            next_state = self.s_err

        return next_state
    
    def s3(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'e':
            next_state = self.s4
            self.value += 'e'
        else:
            next_state = self.s_err

        return next_state
    
    def s4(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 's':
            next_state = self.s5
            self.value += 's'
        else:
            next_state = self.s_err

        return next_state
    
    
    def s5(self) -> function:
        next_state: function = self.s5 # if any inputs, go to error state
        self.num_chars_read += 1
        return next_state
    
    
    def s_err(self) -> function:
        next_state = self.s_err 
        self.num_chars_read += 1
        return next_state