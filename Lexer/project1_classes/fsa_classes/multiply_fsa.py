from .fsa import FSA

class MULTIPLYFSA(FSA):
    def __init__(self):
        FSA.__init__(self,"MultiplyFSA") # You must invoke the __init__ of the parent class
        self.accept_states.add(self.s1) 
        self.token_name = "MULTIPLY"
    
    def s0(self):
        current_input: str = self._FSA__get_current_input()
        next_state: function = None
        if current_input == '*':
            next_state: function = self.s1
            self.value += "*"
        else:
            next_state: function = self.s_err
        return next_state

    def s1(self):
        current_input: str = self._FSA__get_current_input()
        next_state: function = self.s1  # loop in state s1
        return next_state

    def s_err(self):
        current_input: str = self._FSA__get_current_input()
        next_state: function = self.s_err  # loop in state serr
        return next_state