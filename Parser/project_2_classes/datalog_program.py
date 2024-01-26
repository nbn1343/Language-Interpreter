class DatalogProgram:
    def __init__(self, schemes, facts, rules, queries):
        self.schemes = schemes
        self.facts = facts
        self.rules = rules
        self.queries = queries
        self.domain = set()

    def to_string(self):
        program_str = "Schemes(" + str(len(self.schemes)) + "):\n"
        for scheme in self.schemes:
            program_str += "  " + scheme + "\n"

        program_str += "Facts(" + str(len(self.facts)) + "):\n"
        for fact in self.facts:
            program_str += "  " + fact + "\n"

        program_str += "Rules(" + str(len(self.rules)) + "):\n"
        for rule in self.rules:
            program_str += "  " + rule + "\n"

        program_str += "Queries(" + str(len(self.queries)) + "):\n"
        for query in self.queries:
            program_str += "  " + query  + "\n"

        # program_str += "Domain(" + str(len(self.domain)) + "):\n"
        # for item in sorted(self.domain):
        #     program_str += "  " + item + "\n"

        return program_str


    # def generate_domain(self):
    #     for fact in self.facts:
    #         for value in fact.split(','):
    #             for v in value.split("("):
    #                 for i in v.split(")"):
    #                     if "'" in i:
    #                         self.domain.add(i.strip())

        