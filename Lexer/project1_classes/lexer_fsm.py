from typing import Callable as function
from typing import List

from .fsa_classes.fsa import FSA
from .fsa_classes.colon_dash_fsa import ColonDashFSA
from .fsa_classes.colon_fsa import ColonFSA
from .fsa_classes.right_paren_fsa import RightParenFSA
from .fsa_classes.left_paren_fsa import LeftParenFSA
from .fsa_classes.period_fsa import PeriodFSA
from .fsa_classes.q_mark_fsa import Q_MARKFSA
from .fsa_classes.comma_fsa import COMMAFSA
from .fsa_classes.multiply_fsa import MULTIPLYFSA
from .fsa_classes.add_fsa import ADD_FSA
from .fsa_classes.schemes_fsa import SCHEMES_FSA
from .fsa_classes.rules_fsa import RULES_FSA
from .fsa_classes.queries_fsa import QUERIES_FSA
from .fsa_classes.facts_fsa import FACTS_FSA
from .fsa_classes.id_fsa import ID_FSA
from .fsa_classes.comment_fsa import COMMENT_FSA
from .fsa_classes.string_fsa import STRING_FSA

from .token import Token


# class Token:
#     def __init__(self, token_type, value, line_number):
#         self.token_type = token_type
#         self.value = value
#         self.line_number = line_number

#     def __str__(self):
#         return f'({self.token_type},"{self.value}",{self.line_number})'

class LexerFSM:
    def __init__(self):
        self.tokens: List[Token] = []

        self.right_paren_fsa: RightParenFSA = RightParenFSA()
        self.left_paren_fsa: LeftParenFSA = LeftParenFSA()     
        self.colon_fsa: ColonFSA = ColonFSA()
        self.colon_dash_fsa: ColonDashFSA = ColonDashFSA()
        self.period_fsa: PeriodFSA = PeriodFSA()
        self.qmark_fsa: Q_MARKFSA = Q_MARKFSA()
        self.comma_fsa: COMMAFSA = COMMAFSA()
        self.mult_fsa: MULTIPLYFSA = MULTIPLYFSA()
        self.add_fsa: ADD_FSA = ADD_FSA()
        self.schemes_fsa: SCHEMES_FSA = SCHEMES_FSA()
        self.rules_fsa: RULES_FSA = RULES_FSA()
        self.queries_fsa: QUERIES_FSA = QUERIES_FSA()
        self.facts_fsa: FACTS_FSA = FACTS_FSA()
        self.id_fsa: ID_FSA = ID_FSA()
        self.comment_fsa: COMMENT_FSA = COMMENT_FSA()
        self.string_fsa: STRING_FSA = STRING_FSA()

        self.fsa_keys: list[function] = [self.right_paren_fsa, self.left_paren_fsa,self.colon_fsa, self.colon_dash_fsa, self.period_fsa, self.qmark_fsa, self.comma_fsa, self.mult_fsa, self.add_fsa, self.schemes_fsa, self.rules_fsa, self.queries_fsa, self.facts_fsa, self.id_fsa, self.comment_fsa, self.string_fsa]
        self.fsa_dict: dict[function, bool] = dict.fromkeys(self.fsa_keys, False)

    def lex(self, input_string: str) -> function:
        tokens = []
        self.line_num = 1
        input = input_string

        while len(input) > 0:
            if input[0].isspace() or input[0] == "\n":
                if input[0] == "\n":
                    self.line_num += 1
                input = input[1:]
                continue

            token_value = ""
            tracker = 0
            matched = False  

            for FSA in self.fsa_dict.keys():
                FSA.reset()
                self.fsa_dict[FSA] = FSA.run(input)
            
                if self.fsa_dict[FSA] == True:
                    if len(FSA.value) > tracker:
                        tracker = len(FSA.value)
                        token_value = FSA.value

                    matched = True

            if not matched:
                token_value = input[0]
                tracker = 1

            # token_1 = f'({self.__manager_fsm__()},"{token_value}",{self.line_num})'
            token = Token(self.__manager_fsm__(),token_value,self.line_num)
            tokens.append(token)
            if "UNDEFINED" == token.token_type:
                # tokens.append(token)
                return tokens
            input = input[tracker:]


        return tokens
    
    def __manager_fsm__(self) -> str:
        
        max_length = 0
        max_fsa = "UNDEFINED"
        for fsa in self.fsa_dict.keys():
             if self.fsa_dict[fsa] == True:
                  if len(fsa.value) > max_length:
                        max_length = len(fsa.value)
                        max_fsa = fsa.token_name 
        return max_fsa
    
        

    def reset(self) -> None:
        for FSA in self.fsa_dict.keys(): FSA.reset()