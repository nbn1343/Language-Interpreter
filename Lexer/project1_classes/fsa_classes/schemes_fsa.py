from .fsa import FSA
from typing import Callable as function

class SCHEMES_FSA(FSA):
    def __init__(self):
        FSA.__init__(self, "Schemes") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s7)
        self.token_name = "SCHEMES"
    
    def s0(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'S':
            next_state = self.s1
            self.value += "S"
        else:
            next_state = self.s_err

        return next_state

    def s1(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'c':
            next_state = self.s2
            self.value += "c"
        else:
            next_state = self.s_err

        return next_state
    
    def s2(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'h':
            next_state = self.s3
            self.value += "h"
        else:
            next_state = self.s_err

        return next_state
    
    def s3(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'e':
            next_state = self.s4
            self.value += "e"
        else:
            next_state = self.s_err

        return next_state
    
    def s4(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'm':
            next_state = self.s5
            self.value += "m"
        else:
            next_state = self.s_err

        return next_state
    
    def s5(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'e':
            next_state = self.s6
            self.value += "e"
        else:
            next_state = self.s_err

        return next_state
    
    def s6(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 's':
            next_state = self.s7
            self.value += "s"
        else:
            next_state = self.s_err

        return next_state
    
    
    def s7(self) -> function:
        next_state: function = self.s7 
        self.num_chars_read += 1
        return next_state
    
    
    def s_err(self) -> function:
        #print("In state s_err. s_err's information is ",self.s_err)
        next_state = self.s_err # stay in error state on all inputs
        self.num_chars_read += 1
        return next_state