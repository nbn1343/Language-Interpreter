from .fsa import FSA
from typing import Callable as function

class ColonDashFSA(FSA):
    def __init__(self):
        FSA.__init__(self, "Colon-Dash")
        self.accept_states.add(self.s2)
        self.token_name = "COLON_DASH"
    
    def s0(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == ':':
            next_state = self.s1
            self.value += ":"
        else:
            next_state = self.s_err

        return next_state

    def s1(self) -> function:
        
        current_input: str = self._FSA__get_current_input()
        next_state: function = None

        if current_input == '-':
            next_state = self.s2
            self.value += "-"
        else:
            next_state = self.s_err

        return next_state
    
    def s2(self) -> function:
        current_input: str = self._FSA__get_current_input()
        next_state: function = self.s2 # if any inputs, go to error state
        self.num_chars_read += 1
        return next_state
    
    def s_err(self) -> function:
        #print("In state s_err. s_err's information is ",self.s_err)
        next_state = self.s_err # stay in error state on all inputs
        self.num_chars_read += 1
        return next_state
    
    
    

# my_fsa: ColonDashFSA = ColonDashFSA("Colon_dash")
# input_string: str = ":-"
# accept_status: bool = my_fsa.run(input_string)
# if accept_status: print("The ", my_fsa.get_name(), "FSA accepted the input string '", input_string, "'")
# else: print("The ", my_fsa.get_name(), "FSA did not accept the input string '", input_string, "'")