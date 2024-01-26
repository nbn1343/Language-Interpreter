class Rule:
    def __init__(self, head_predicate, body_predicates):
        self.head_predicate = head_predicate
        self.body_predicates = body_predicates

    def to_string(self):
        body_str = ",".join(map(str, self.body_predicates))
        return f"{self.head_predicate} :- {body_str}."