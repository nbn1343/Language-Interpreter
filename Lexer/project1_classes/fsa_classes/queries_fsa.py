from .fsa import FSA
from typing import Callable as function

class QUERIES_FSA(FSA):
    def __init__(self):
        FSA.__init__(self, "Queries") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s7)
        self.token_name = "QUERIES"
    
    def s0(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'Q':
            next_state = self.s1
            self.value += "Q"
        else:
            next_state = self.s_err

        return next_state

    def s1(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'u':
            next_state = self.s2
            self.value += "u"
        else:
            next_state = self.s_err

        return next_state
    
    def s2(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'e':
            next_state = self.s3
            self.value += "e"
        else:
            next_state = self.s_err

        return next_state
    
    def s3(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'r':
            next_state = self.s4
            self.value += "r"
        else:
            next_state = self.s_err

        return next_state
    
    def s4(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == 'i':
            next_state = self.s5
            self.value += "i"
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