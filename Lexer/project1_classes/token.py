class Token:
    def __init__(self, token_type, value, line_number):
        self.token_type = token_type
        self.value = value
        self.line_number = line_number

    def to_string(self) -> str:
        return self.__str__()

    def __str__(self):
        return "(" + self.token_type + "," + '"' + self.value + '"' + "," + str(self.line_number) + ")"