from .my_token import Token
from .predicate import Predicate
from .parameter import Parameter
from .rule import Rule
from .datalog_program import DatalogProgram


class Parser():
    def __init__(self):
        self.datalog_program = None

    def get_program(self):
        return self.datalog_program



    def throw_error(self):
        raise ValueError(self.get_curr_token().to_string())


    def get_curr_token(self) -> Token:
        if self.index >= len(self.tokens):
            self.index = len(self.tokens) - 1
            self.throw_error()
        return self.tokens[self.index]
    

    def get_prev_token_value(self) -> str:
        return self.tokens[self.index - 1].value
        

    def advance(self):
        self.index += 1

    def match(self, expected_type: str):
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == expected_type:
            self.advance()
        else:
            self.throw_error()


    def run(self, tokens: list[Token]) -> str:
        self.index: int = 0
        self.tokens: list[Token] = tokens

        try:
            datalog_program = self.parse_datalog_program()
            # datalog_program.generate_domain()
            return datalog_program
        except ValueError as ve:
            return f"Failure!\n  {ve}"
        


    def parse_datalog_program(self):
        schemes = []
        facts = []
        rules = []
        queries = []

        self.match("SCHEMES")
        self.match("COLON")
        schemes.append(self.parse_scheme())
        schemes += self.parse_scheme_list()

        self.match("FACTS")
        self.match("COLON")
        facts = self.parse_fact_list()

        self.match("RULES")
        self.match("COLON")
        rules = self.parse_rule_list()

        self.match("QUERIES")
        self.match("COLON")
        queries.append(self.parse_query())
        queries += self.parse_query_list()

        return DatalogProgram(schemes, facts, rules, queries)



    def parse_scheme_list(self):
        scheme_list = []
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "ID":
            # self.parse_scheme()
            scheme_list.append(self.parse_scheme())

            scheme_list += self.parse_scheme_list()

            return scheme_list
        else:
            return ""


    def parse_fact_list(self):
        fact_list = []
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "ID":
            fact_list.append(self.parse_fact())

            fact_list += self.parse_fact_list()

            return fact_list
        else:
            return ""


    def parse_rule_list(self):
        rule_list = []
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "ID":
            rule_list.append(self.parse_rule())

            rule_list += self.parse_rule_list()

            return rule_list
        else:
            return ""


    def parse_query_list(self):
        query_list = []
        if self.index >= len(self.tokens):
            return ""
        while self.get_curr_token().token_type == "COMMENT" and self.index != len(self.tokens) - 1:
            self.advance()
        if self.get_curr_token().token_type == "ID":
            query_list.append(self.parse_query())

            query_list += self.parse_query_list()

            return query_list
        else:
            return ""


    def parse_scheme(self) -> Predicate:
        name = ""
        parameters: list[str] = []

        self.match("ID")
        name = self.get_prev_token_value()

        self.match("LEFT_PAREN")

        self.match("ID")
        parameters.append(self.get_prev_token_value())

        parameters += self.parse_id_list()
        self.match("RIGHT_PAREN")
        parsed_scheme = Predicate(name, parameters)

        return parsed_scheme


    def parse_fact(self) -> Parameter:
        name = ""
        parameters: list[str] = []

        self.match("ID")
        name = self.get_prev_token_value()
        self.match("LEFT_PAREN")
        self.match("STRING")
        parameters.append(self.get_prev_token_value())
        
        parameters += self.parse_string_list()

        self.match("RIGHT_PAREN")
        self.match("PERIOD")
        
        fact_parsed = Parameter(name, parameters)
        return fact_parsed

    def parse_rule(self):
        head_predicate = ""
        body_predicates: list[str] = []
        head_predicate = self.parse_head_predicate()
        self.match("COLON_DASH")
        body_predicates.append(self.parse_predicate())
        body_predicates += self.parse_predicate_list()
        self.match("PERIOD")

        parsed_rule = Rule(head_predicate,body_predicates)

        return parsed_rule

    def parse_query(self):
        parsed_query = self.parse_predicate()
        self.match("Q_MARK")
        # parsed_query += self.get_prev_token_value()

        return parsed_query
        

    def parse_id_list(self) -> list[str]:
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("ID")
            curr_id: list[str] = [self.get_prev_token_value()]

            rest_ids:list[str] = self.parse_id_list()

            return curr_id + rest_ids
        
        else:
            return []

    def parse_string_list(self):
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("STRING")
            self.parse_string_list()
        else:
            return

    def parse_predicate_list(self):
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            curr_id: list[str] = [self.parse_predicate()]

            rest_ids:list[str] = self.parse_predicate_list()

            return curr_id + rest_ids
        else:
            return []

    def parse_head_predicate(self):
        name = ""
        parameters: list[str] = []
        self.match("ID")
        name = self.get_prev_token_value()
        self.match("LEFT_PAREN")
        self.match("ID")
        parameters.append(self.get_prev_token_value())
        parameters += self.parse_id_list()
        self.match("RIGHT_PAREN")

        parsed_head = Predicate(name,parameters)

        return parsed_head

    def parse_predicate(self):
        name = ""
        parameters: list[str] = []

        self.match("ID")
        name = self.get_prev_token_value()

        self.match("LEFT_PAREN")
        self.parse_parameter()
        parameters.append(self.get_prev_token_value())
        parameters += self.parse_parameter_list()
        self.match("RIGHT_PAREN")

        parsed_predicate = Predicate(name, parameters)

        return parsed_predicate


    def parse_parameter_list(self):
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.parse_parameter()
            curr_id: list[str] = [self.get_prev_token_value()]

            rest_ids:list[str] = self.parse_parameter_list()

            return curr_id + rest_ids
        else:
            return []

    def parse_parameter(self):
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "STRING":
            self.match("STRING")
        elif self.get_curr_token().token_type == "ID":
            self.match("ID")
        else:
            self.throw_error()

    def parse_string_list(self):
        while self.get_curr_token().token_type == "COMMENT":
            self.advance()
        if self.get_curr_token().token_type == "COMMA":
            self.match("COMMA")
            self.match("STRING")
            curr_id: list[str] = [self.get_prev_token_value()]

            rest_ids:list[str] = self.parse_string_list()

            return curr_id + rest_ids
        else:
            return []

    