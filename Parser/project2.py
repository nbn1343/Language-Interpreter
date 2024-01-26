from project_2_classes.my_token import Token
from Parser.project_2_classes.parser import Parser
from Lexer.project1_classes.lexer_fsm import LexerFSM


def project2(input: str) -> str:
    lexer = LexerFSM()
    tokens = lexer.lex(input)

    parser = Parser()

    return parser.run(tokens)


def read_file_contents(filepath):
    with open(filepath, "r") as f:
        return f.read()


# Use this to run and debug code within VS
if __name__ == "__main__":
    input_contents = read_file_contents("./project-2-nbn1343/Parser/project2-passoff/100/input0.txt")
    
    print(project2(input_contents))
